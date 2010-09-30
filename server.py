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

from tornado.options import define, options

import urllib
from elementtree.ElementTree import parse

define("debug", default=False, help="debug mode", type=bool)
define("appbundle", default=True, help="indicates if running in Mac OSX app bundle", type=bool)
define("working_folder", default=os.path.dirname(__file__), help="the folder to look for all the files", type=str)
define("clean_install", default=False, help="erase non-user data from app support folder", type=bool)



#========================================================
def debug_print(*arguments):
	if options.debug:
		for arg in arguments: 
			print arg,
		print
		
#========================================================
class Application(tornado.web.Application):
	
	password = "changeme"
	port = 8888

	# by default, working folder is where the script lives
	working_folder = options.working_folder

	bb_folder = "bb"
	image_folder = "images"
	custom_image_folder = "user/customimages"
	custom_scripts_folder = "user/customscripts"
	
	def __init__(self):

		if options.appbundle == True:
			debug_print("Running as Mac OSX app bundle")
			self.setup_mac_files()
		
		debug_print("working_folder = " + self.working_folder)

		self.read_settings_file()

		#pre-load the xml cmd list and layout

		xml_cmds = []
		xml_rows = []

		if os.path.exists(os.path.join(self.working_folder, "user/customxml/cmds.xml")):
			xml_data = parse(os.path.join(self.working_folder, "user/customxml/cmds.xml")).getroot()
			xml_cmds.extend(xml_data.findall('cmds/cmd'))
			xml_rows = xml_data.findall('layout/buttonrow')
			debug_print( "Adding commands from custom file")
		
		xml_data = parse(os.path.join(self.working_folder, "xml/cmds.xml")).getroot()
		xml_cmds.extend(xml_data.findall('cmds/cmd'))

		#only use the layout from this file if the previous is missing on
		if len(xml_rows) == 0:
			xml_rows = xml_data.findall('layout/buttonrow')
			debug_print( "Using default layout")
		else:
			debug_print( "Using custom layout")
		
		
		handlers = [
			(r"/", MainHandler),
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
			working_folder = self.working_folder,
			xml_cmds = xml_cmds,
			xml_rows = xml_rows,
			bb_folder = self.bb_folder,
			image_folder = self.image_folder,
			custom_image_folder = self.custom_image_folder,
		)
		tornado.web.Application.__init__(self, handlers, **settings)
		sys.stdout.flush()
#------------------------
	def read_settings_file(self):
	
		#read custom settings file if it exists
		xml_data = None
		
		try: 
			xml_data = parse(os.path.join(self.working_folder, "user/customxml/settings.xml")).getroot()
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
				
		debug_print("The password = ", self.password)
		debug_print("The port = " , self.port)
	
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
				list = glob.glob(self.working_folder + "/[a-t,v-z,A-Z]*")
				for item in list:
					debug_print ("Going to remove "+item)
					if os.path.isdir(item):
						shutil.rmtree(item)
					else:
						os.remove(item)
					
	
		debug_print ("Copying files over from app bundle")
		self.copyover("bb")
		self.copyover("static")
		self.copyover("scripts")
		self.copyover("templates")
		self.copyover("images")
		self.copyover("xml")
		self.copyover("user")

#========================================================

def custom_get_current_user(handler):
	if handler.get_secure_cookie("auth"):
		if handler.get_secure_cookie("auth") == handler.application.password:
			return "theuser"
	else:
		return None



#========================================================
class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return custom_get_current_user(self)

#========================================================
class MainHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		table = self.html_grid()
		self.render("index.html", table = table)

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

								tmp = cmd.find("icon")
								if not tmp == None and not tmp.text.strip() == "":
									icon = tmp.text
								else:
									icon = "/images/buttonboard.png"

								tmp = cmd.find("badge")
								if not tmp == None and not tmp.text.strip() == "":
									badge = tmp.text
								else:
									badge = None

								elementHTML += "\t\t\t<div class=\"imagescaler\">\n"
								elementHTML += "\t\t\t\t<img class=\"layer\" src=\"" + icon + "\" />\n"
								if not badge == None:
									elementHTML += "\t\t\t\t<img class=\"badge\" src=\"" + badge + "\" />\n"
								
									
								elementHTML += "\t\t\t\t<a href=\"#\"><img class=\"layer\" src=\""
								elementHTML += "/images/button_mask.png"
								elementHTML += "\" onclick=\"run_cmd('" 
								elementHTML += cmd_name 
								elementHTML += "','"
								elementHTML += confirm
								elementHTML += "','"
								elementHTML += output
								elementHTML += "')\" /></a>\n" 	
								elementHTML += "\t\t\t</div>\n"
							else:
								tmp = cmd.find("label")
								if not tmp == None and not tmp.text.strip() == "":
									label = tmp.text
								else:
									label = cmd_name
									
								elementHTML = "\t\t\t" + label + "\n"
					table +=  "\t\t<td>\n" + elementHTML + "\t\t</td>\n"			
				table +=  "\t</tr>\n"
				
		return table

	

#========================================================
class LoginHandler(BaseHandler):
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
	@tornado.web.authenticated
	def get(self, cmd):
		word_list = self.get_cmd_script_and_args(cmd)
		debug_print(word_list)
		if len(word_list) > 0 :
			working_folder = self.application.settings["working_folder"]
			script_with_path = os.path.join(working_folder, word_list[0])
			word_list[0] = script_with_path
			cmd_output = Popen(word_list, stdout=PIPE).communicate()[0]
		else:
			cmd_output = "Command not found"
		debug_print (cmd_output)
		self.write( "Done: \n" + cmd_output )
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
					
					for param_item in script_item.findall('param'):
						word_list.append(param_item.text.strip())	
				
				return word_list

		return word_list

#========================================================
		
class AuthStaticFileHandler(tornado.web.StaticFileHandler):

	@tornado.web.authenticated
	def get(self, path):
		tornado.web.StaticFileHandler.get(self, path)

	def get_current_user(self):
		#call global version used by other classes
		return custom_get_current_user(self)

#========================================================
		
class ButtonBoardStaticFileHandler(AuthStaticFileHandler):

	def __init__(self, application, request, **kwargs):
		tornado.web.RequestHandler.__init__(self, application, request)
		working_folder = application.settings["working_folder"]
		self.root = os.path.abspath(os.path.join(working_folder, application.settings["bb_folder"]))

#========================================================
		
class ImageStaticFileHandler(AuthStaticFileHandler):

	def __init__(self, application, request, **kwargs):
		tornado.web.RequestHandler.__init__(self, application, request)
		working_folder = application.settings["working_folder"]
		self.root = os.path.abspath(os.path.join(working_folder, application.settings["image_folder"]))


#========================================================
		
class CustomImageStaticFileHandler(AuthStaticFileHandler):

	def __init__(self, application, request, **kwargs):
		tornado.web.RequestHandler.__init__(self, application, request)
		working_folder = application.settings["working_folder"]
		self.root = os.path.abspath(os.path.join(working_folder, application.settings["custom_image_folder"]))




#========================================================
def main():
	tornado.options.parse_command_line()
	theApp = Application()
	http_server = tornado.httpserver.HTTPServer(theApp)
	http_server.listen(theApp.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

