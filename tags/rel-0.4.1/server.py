#!/usr/bin/env python
#
import sys 
import glob 
import os.path
import getpass
import shutil
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from subprocess import *
from time import localtime, strftime

from tornado.options import define, options

import urllib
from elementtree.ElementTree import parse

# Slightly different import for ubuntu 10.04
#from xml.etree.ElementTree import parse

try:
	from imageresizer import Resizer
except:
	print("Couldn't import Resizer");	

define("debug", default=False, help="debug mode", type=bool)
define("appbundle", default="auto", help="indicates if running in Mac OSX app bundle", type=str)
define("working_folder", default=os.path.dirname(__file__), help="the folder to look for all the files", type=str)
define("clean_install", default=True, help="erase non-user data from app support folder", type=bool)

print("Tornado Version = " + tornado.version)

#========================================================
"""
HELPER FUNCS
"""

def debug_print(*arguments):
	if options.debug:
		for arg in arguments: 
			print arg,
		print
		
def str2bool(v):
	return v.lower() in ["yes", "true", "t", "1"]
	
	
def find_image(custom_path, default_path, name):
	if os.path.exists(os.path.join(custom_path, name)):
		return "/customimages/" + name
	elif os.path.exists(os.path.join(default_path, name)):
		return "/images/" + name
	return "/images/buttonboard.png"
	
		
#========================================================
class Application(tornado.web.Application):

	password = "changeme"
	port = 8888
	wakerurl = ""

	# by default, working folder is where the script lives
	working_folder = options.working_folder

	bb_folder = "bb"
	default_image_folder = "default/images"
	default_script_folder ="default/scripts"
	custom_image_folder = "user/images"
	custom_script_folder = "user/scripts"

	default_cmds_file = "default/cmds.xml"
	custom_cmds_file = "user/cmds.xml" 

	settings_file = "user/settings.xml"

	
	def __init__(self):

		inbundle = False;
		if options.appbundle == "auto":
			#check if the path of this file is in an app bundle kind of path
			if os.path.abspath(os.path.dirname(__file__)).find(".app/Contents/Resources") != -1:
				inbundle = True;
		else:
			inbundle = str2bool(options.appbundle)
		
		if inbundle == True:
			debug_print("Running as Mac OSX app bundle")
			self.setup_mac_files()
		
		print("working_folder = " + self.working_folder)
		
		#the working folder is known, so set up all the path strings now

		self.bb_folder_path = os.path.join(self.working_folder, self.bb_folder)

		self.default_image_path = os.path.join(self.working_folder, self.default_image_folder)
		self.default_script_path = os.path.join(self.working_folder, self.default_script_folder)

		self.custom_image_path = os.path.join(self.working_folder, self.custom_image_folder)
		self.custom_script_path = os.path.join(self.working_folder, self.custom_script_folder)

		self.custom_cmds_file_path = os.path.join(self.working_folder, self.custom_cmds_file)
		self.default_cmds_file_path = os.path.join(self.working_folder, self.default_cmds_file)

		self.settings_file_path = os.path.join(self.working_folder, self.settings_file)


		self.read_settings_file()

		#pre-load the xml cmd list and layout

		xml_cmds = []
		xml_rows = []

		if os.path.exists(self.custom_cmds_file_path):
			xml_data = parse(self.custom_cmds_file_path).getroot()
			xml_cmds.extend(xml_data.findall('cmds/cmd'))
			xml_rows = xml_data.findall('layout/buttonrow')
			debug_print( "Adding commands from custom file")
		
		xml_data = parse(self.default_cmds_file_path).getroot()
		xml_cmds.extend(xml_data.findall('cmds/cmd'))

		#only use the layout from this file if the previous is missing on
		if len(xml_rows) == 0:
			xml_rows = xml_data.findall('layout/buttonrow')
			debug_print( "Using default layout")
		else:
			debug_print( "Using custom layout")
		
		
		handlers = [
			(r"/", MainHandler),
			(r"/ButtonBoard.manifest", ManifestHandler),
			(r"/cmd/([a-zA-Z0-9_]+)", CmdHandler),
			(r"/login", LoginHandler),
			(r"/bb/(.*)", ButtonBoardStaticFileHandler),
			(r"/images/(.*)", ImageStaticFileHandler),
			(r"/customimages/(.*)", CustomImageStaticFileHandler),

		]
		settings = dict(
			cookie_secret="13oETzkxqagAyDKl4GEzGeJDJFuYhdhetr2htwjdhewjdhewj2XdTP1o/Vo=",
			template_path=os.path.join(self.working_folder, "templates"),
			static_path=os.path.join(self.working_folder, "static"),
			xsrf_cookies=True,
			debug=True,
			login_url = "/login",
			xml_cmds = xml_cmds,
			xml_rows = xml_rows,
		)
		
		#Resize images to better size for serving.  Preserves the originals
		try:
			#Resizer(self.default_image_path, "originals").resize()
			Resizer(self.custom_image_path, "originals").resize()
		except:
			print("Automatic resizing of source images not available!!");
			print("You may want to manually resize your images down to 128x128 to speed page loads");
	
	
		self.generate_cache_manifest(xml_cmds, xml_rows)
	
		tornado.web.Application.__init__(self, handlers, **settings)
		sys.stdout.flush()
#------------------------
	def read_settings_file(self):
	
		#read custom settings file if it exists
		xml_data = None
		
		try: 
			xml_data = parse(self.settings_file_path).getroot()
		except:
			debug_print ("Couldn't find or read custom settings file")

		if not xml_data == None	:
			try: 
				self.password = xml_data.find('password').text
			except:
				pass

			try: 
				self.port = int(xml_data.find('port').text)
			except:
				pass
				
			try: 
				self.wakerurl = xml_data.find('wakerurl').text
			except:
				pass
				
		debug_print("The password = ", self.password)
		print "Running on port: " , self.port
	
#------------------------
	# Copy files from app bundle to user L/AS
	def copyover(self, dirname):

		bundle = options.working_folder
		if not os.path.exists(self.working_folder+ os.sep + dirname):
			shutil.copytree( bundle + os.sep + dirname, self.working_folder + os.sep + dirname)

#------------------------

	def setup_mac_files(self):

		self.working_folder = "/Users/" +  getpass.getuser() + "/Library/Application Support/ButtonBoard"

		if not os.path.exists(self.working_folder):
   			os.makedirs(self.working_folder)
			debug_print("Creating " , self.working_folder)

		if options.clean_install:
			debug_print( "Clean install.  Removing all but user folder")
			if os.path.isdir(self.working_folder):
				shutil.rmtree(self.working_folder+"/bb", ignore_errors=True)
				shutil.rmtree(self.working_folder+"/static", ignore_errors=True)
				shutil.rmtree(self.working_folder+"/templates", ignore_errors=True)
				shutil.rmtree(self.working_folder+"/default", ignore_errors=True)
	
		debug_print ("Copying files over from app bundle")
		self.copyover("bb")
		self.copyover("static")
		self.copyover("templates")
		self.copyover("default")
		self.copyover("user")

#---------------------
	def generate_cache_manifest(self, cmds, rows):
		manifest = open(os.path.join(self.working_folder, "ButtonBoard.manifest"), "w")

		manifest.write("CACHE MANIFEST\n")
		#manifest.write("/static/images/splash.png\n")
		manifest.write("/static/images/buttonboard.png\n")
		manifest.write("/bb/ButtonBoard.js\n")
		manifest.write("/bb/ButtonBoard.css\n")
		manifest.write("/images/loading2.gif\n")
		manifest.write("/images/button_mask.png\n")
		manifest.write("/images/mask2.png\n")

		#walk the XML to figure out which specific images to cache
		filelist = []
		for cmd in cmds:
			# see if cmd is in the layout
			for row in rows:
				items = row.findall('item')			
				for item in items:
					layout_name = item.get("n")
					cmd_name = cmd.get("name")
					try: 
						if cmd_name == layout_name:
							# a match!  add icon and badge to list
							icon = cmd.find("icon").text
							if not icon == None:
								icon = find_image(self.custom_image_path, self.default_image_path, icon)
								filelist.append(icon)

							badge = cmd.find("badge").text
							if not badge == None:
								badge = find_image(self.custom_image_path, self.default_image_path, badge)
								filelist.append(badge)
					except:
						pass
				
		#Remove dupes
		filelist = list(set(filelist))

		for f in filelist:
			manifest.write(f+"\n")
			
		manifest.write("\n")
		manifest.write("NETWORK:\n")
		manifest.write("*\n")
		manifest.write("/cmd\n")
		manifest.write("# Generated: " + strftime("%a, %d %b %Y %H:%M:%S +0000", localtime()) + "\n")
		manifest.close()
		
		
		
#========================================================

def custom_get_current_user(handler):
	if handler.get_secure_cookie("auth"):
		if handler.get_secure_cookie("auth") == handler.application.password:
			return "theuser"
	else:
		return None



#========================================================
class BaseHandler(tornado.web.RequestHandler):
	def initialize(self):
		pass

	def get_current_user(self):
		return custom_get_current_user(self)

#========================================================
class MainHandler(BaseHandler):
	def initialize(self):
		pass

	@tornado.web.authenticated
	def get(self):
		table = self.html_grid()
		self.render("index.html", table = table, wakerurl=self.application.wakerurl)

	def html_grid(self):
		table = ""
		cmds = self.application.settings["xml_cmds"]
		rows = self.application.settings["xml_rows"]
		for row in rows:
			# make two passes for each row, icon and label
			for i in [1, 2]:
				table += "\t<tr>\n"
				items = row.findall('item')			
				for item in items:
					cmd_name = item.get("n")
					elementHTML = ""
					onclick = ""
					#search in command list
					for cmd in cmds:
						if cmd_name == cmd.get("name"):
							if i == 1:								
								tmp = cmd.find("output")
								if not tmp == None and tmp.text.strip().lower() == "true":
									output = "true"
								else:
									output = "false"
									
								tmp = cmd.find("confirm")	
								if not tmp == None and tmp.text.strip().lower() == "true":
									confirm = "true"
								else:
									confirm = "false"

								tmp = cmd.find("label")	
								if not tmp == None:
									label = tmp.text
								else:
									label = ""

								tmp = cmd.find("icon")
								if not tmp == None and not tmp.text.strip() == "":
									icon = find_image(self.application.custom_image_path, self.application.default_image_path, tmp.text)
								else:
									icon = "/images/buttonboard.png"

								tmp = cmd.find("badge")
								if not tmp == None and not tmp.text.strip() == "":
									badge = find_image(self.application.custom_image_path, self.application.default_image_path, tmp.text)
								else:
									badge = None

								onclick += " onclick=\"run_cmd('" 
								onclick += cmd_name 
								onclick += "','"
								onclick += label 
								onclick += "','"
								onclick += confirm
								onclick += "','"
								onclick += output
								onclick += "')\" " 	

								elementHTML += "\t\t\t<div class=\"imagescaler\">\n"
								elementHTML += "\t\t\t\t<img class=\"layer\" src=\"" + icon + "\" />\n"
								elementHTML += "\t\t\t\t<img class=\"layer\" src=\"images/mask2.png\" />\n"
								if not badge == None:
									elementHTML += "\t\t\t\t<img class=\"badge\" src=\"" + badge + "\" />\n"
								
								elementHTML += "\t\t\t\t<img class=\"layer\" src=\""
								elementHTML += "/images/button_mask.png"
								elementHTML += "\"  />\n" 	
								elementHTML += "\t\t\t</div>\n"

							else:
								tmp = cmd.find("label")
								if not tmp == None and not tmp.text.strip() == "":
									label = tmp.text
								else:
									label = cmd_name
									
								elementHTML = "\t\t\t" + label + "\n"
					table +=  "\t\t<td" + onclick +  ">\n" + elementHTML + "\t\t</td>\n"			
				table +=  "\t</tr>\n"
				
		return table

#========================================================
		
class ManifestHandler(BaseHandler):
	def initialize(self):
		pass

	def get(self):
		self.set_header("Content-Type", "text/cache-manifest")
		manifest = open(os.path.join(self.application.working_folder, "ButtonBoard.manifest"), "r")
		self.write(manifest.read())

#========================================================
class LoginHandler(BaseHandler):
	def initialize(self):
		pass

	def get(self):
		if  len(self.get_arguments("next")) != 0:
			next=self.get_argument("next")
		else:
			next="/"
		self.render('login.html', next=next)
#------------------------
	def post(self):
		
		next = self.get_argument("next")

		if  len(self.get_arguments("password")) != 0:
			
			if self.get_argument("password")  ==  self.application.password:
				self.set_secure_cookie("auth", self.get_argument("password"))
			
		self.redirect(next)


#========================================================
class CmdHandler(BaseHandler):
	def initialize(self):
		pass

	@tornado.web.authenticated
	def get(self, cmd):
		status = "Done"
		word_list = self.get_cmd_script_and_args(cmd)
		debug_print(word_list)
		if len(word_list) > 0 :
			script_with_path = self.find_file(word_list[0])
			if (script_with_path):
				word_list[0] = script_with_path
				cmd_output = Popen(word_list, stdout=PIPE).communicate()[0]
			else:
				status = "Fail"
				cmd_output = "Executable not found"
		else:
			status = "Fail"
			cmd_output = "Command not found"
		debug_print (cmd_output)
		self.write( status + "::" + cmd_output )
		sys.stdout.flush()
#------------------------
	def get_cmd_script_and_args(self, cmd):

		xml_cmds = self.application.settings["xml_cmds"]
		word_list = []

		for item in xml_cmds:
			if  item.get('name') == cmd:
				script_item = item.find("exec")
				if not script_item == None:
					word_list.append(script_item.text.strip())
					
					for param_item in item.findall('param'):
						word_list.append(param_item.text.strip())	
				
				return word_list

		return word_list
#------------------------
	def find_file(self, name):
		#if file name is absolute just use that:
		if os.path.isabs(name):
			return name
		if os.path.exists(os.path.join(self.application.custom_script_path, name)):
			return os.path.join(self.application.custom_script_path, name)
		elif os.path.exists(os.path.join(self.application.default_script_path, name)):
			return os.path.join(self.application.default_script_path, name)
		return None 

		


#========================================================
		
class AuthStaticFileHandler(tornado.web.StaticFileHandler):
	def initialize(self):
		pass

	@tornado.web.authenticated
	def get(self, path):
		tornado.web.StaticFileHandler.get(self, path)

	def get_current_user(self):
		#call global version used by other classes
		return custom_get_current_user(self)

#========================================================
		
class ButtonBoardStaticFileHandler(AuthStaticFileHandler):
	def initialize(self):
		pass

	def __init__(self, application, request, **kwargs):
		tornado.web.RequestHandler.__init__(self, application, request)
		self.root = os.path.abspath(application.bb_folder_path)

#========================================================
		
class ImageStaticFileHandler(AuthStaticFileHandler):
	def initialize(self):
		pass

	def __init__(self, application, request, **kwargs):
		tornado.web.RequestHandler.__init__(self, application, request)
		self.root = os.path.abspath(application.default_image_path)


#========================================================
		
class CustomImageStaticFileHandler(AuthStaticFileHandler):
	def initialize(self):
		pass

	def __init__(self, application, request, **kwargs):
		tornado.web.RequestHandler.__init__(self, application, request)
		self.root = os.path.abspath(application.custom_image_path)


#========================================================
def main():
	tornado.options.parse_command_line()
	theApp = Application()
	http_server = tornado.httpserver.HTTPServer(theApp)
	http_server.listen(theApp.port)
	print "Starting web server..." 
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

