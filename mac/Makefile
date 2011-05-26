VERSION_STR="0.4.1"

build: appbundle diskimage

test: clean build install run

appbundle:
	#Generate app bundle with platypus CL tool
	platypus -P ./ButtonBoard.platypus -V $(VERSION_STR) ButtonBoard.app

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
	rm -f ButtonBoard-$(VERSION_STR).dmg
	hdiutil create -srcdir ./ButtonBoard ButtonBoard-$(VERSION_STR)
	

	#remove working files and folders
	rm -rf ButtonBoard

install:
	hdiutil attach ./ButtonBoard-$(VERSION_STR).dmg
	rm -rf /Applications/Buttonboard.app
	cp -a /Volumes/ButtonBoard/ButtonBoard.app /Applications
	hdiutil detach /Volumes/ButtonBoard
	
run:
	 - killall ButtonBoard
	 - killall python
	open /Applications/ButtonBoard.app
	
clean:
	rm -rf ButtonBoard.app ButtonBoard ButtonBoard*.dmg





