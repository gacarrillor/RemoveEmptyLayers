"""
/***************************************************************************
 RemoveEmptyLayers
                                 A QGIS plugin
 This plugin 'cleans' the layer list widget by removing empty layers
                              -------------------
        begin                : 2011-03-06
        copyright            : (C) 2011 by German Carrillo, GeoTux
        email                : geotux_tuxman@linuxmail.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os

# Import the PyQt and QGIS libraries
from qgis.core import QgsApplication, QgsMapLayer, QgsProject
from qgis.PyQt.QtCore import ( QObject, QCoreApplication, QFile, QLocale,
                           QTranslator, QFileInfo, QSettings )
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
# Initialize Qt resources from file resources.py
from .resources_rc import *

class RemoveEmptyLayers:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.installTranslator()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction( QIcon( ":/plugins/removeemptylayers/icon_default.png" ),
            QCoreApplication.translate( "REL", "Remove empty layers" ),
            self.iface.mainWindow() )
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToVectorMenu( QCoreApplication.translate( "REL",
            "&Remove empty layers" ), self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginVectorMenu( QCoreApplication.translate( "REL",
            "&Remove empty layers" ), self.action )
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        toBeRemoved = []
        for key, layer in QgsProject.instance().mapLayers().items():
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.featureCount() == 0:
                    toBeRemoved.append( layer.id() )

        if toBeRemoved:
            QgsProject.instance().removeMapLayers( toBeRemoved )

        msg = ''
        numLayers = len(toBeRemoved)
        if numLayers == 0:
            msg = QCoreApplication.translate( "REL", "There are no empty layers to remove." )
        elif numLayers == 1:
            msg = QCoreApplication.translate( "REL", "One layer has been removed." )
        else:
            msg = str( numLayers ) + QCoreApplication.translate( "REL",
                " layers have been removed." )

        self.iface.messageBar().pushMessage( QCoreApplication.translate( "REL",
              "[Remove empty layers]" ), msg, duration=8 )


    def installTranslator( self ):
        userPluginPath = os.path.join( os.path.dirname( str( QgsApplication.qgisUserDatabaseFilePath() ) ), "python/plugins/RemoveEmptyLayers" )
        systemPluginPath = os.path.join( str( QgsApplication.prefixPath() ), "python/plugins/RemoveEmptyLayers" )
        translationPath = ''

        locale = QSettings().value("locale/userLocale", type=str)
        myLocale = str( locale[0:2] )

        if os.path.exists( userPluginPath ):
            translationPath = os.path.join( userPluginPath, "removeemptylayers_" + myLocale + ".qm" )
        else:
            translationPath = os.path.join( systemPluginPath, "removeemptylayers_" + myLocale + ".qm" )

        if QFileInfo( translationPath ).exists():
            self.translator = QTranslator()
            self.translator.load( translationPath )
            QCoreApplication.installTranslator( self.translator )
