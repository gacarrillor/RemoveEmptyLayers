
all: resources_rc.py removeemptylayers_es.qm

clean:
	rm -f resources_rc.py
	rm -f removeemptylayers_es.qm
	rm -f *.pyc *~

# sudo ln -s /usr/lib/qt6/libexec/rcc /usr/local/bin/rcc
resources_rc.py: resources.qrc
	rcc -g python -o resources_rc.py resources.qrc

# sudo ln -s /usr/lib/qt6/bin/lrelease /usr/local/bin/lrelease
removeemptylayers_es.qm: removeemptylayers_es.ts
	lrelease removeemptylayers_es.ts -qm removeemptylayers_es.qm
