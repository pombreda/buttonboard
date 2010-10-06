VERSION_STR="0.2.2"

all: appbundle diskimage

appbundle:
	#Generate app bundle with platypus CL tool
	platypus -P ./ButtonBoard.platypus ButtonBoard.app

	#Clean out svn junk and other stuff
	find ButtonBoard.app -name .svn |xargs rm -rf
	find ButtonBoard.app -name .DS_Store |xargs rm -rf

diskimage:
	#Set up disk image staging folder
	mkdir -p ButtonBoard
	rm -rf ButtonBoard/*
	cp ../README.txt ButtonBoard
	mv ButtonBoard.app ButtonBoard
	
	#generate disk image
	hdiutil create -srcdir ./ButtonBoard ButtonBoard-$(VERSION_STR)
	

	#remove working files and folders
	rm -rf ButtonBoard

clean:
	rm -rf ButtonBoard.app ButtonBoard ButtonBoard*.dmg





