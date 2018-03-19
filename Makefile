
all: resources_rc.py removeemptylayers_es.qm

clean:
	rm -f resources_rc.py
	rm -f removeemptylayers_es.qm
	rm -f *.pyc *~

resources_rc.py: resources.qrc
	pyrcc5 -o resources_rc.py resources.qrc

removeemptylayers_es.qm: removeemptylayers_es.ts
	lrelease removeemptylayers_es.ts -qm removeemptylayers_es.qm
