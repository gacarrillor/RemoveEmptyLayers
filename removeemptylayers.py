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
from PyQt4.QtCore import ( QObject, SIGNAL, QCoreApplication, QFile, QLocale, 
                           QTranslator, QFileInfo, QSettings )
from PyQt4.QtGui import QMessageBox, QIcon, QAction
from qgis.core import QGis, QgsApplication, QgsMapLayer, QgsMapLayerRegistry
# Initialize Qt resources from file resources.py
import resources

class RemoveEmptyLayers:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.installTranslator()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction( self.getThemeIcon(), QCoreApplication.translate( "REL", 
            "Remove empty layers" ), self.iface.mainWindow() )
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu( QCoreApplication.translate( "REL", 
            "&Remove empty layers" ), self.action)

        QObject.connect(self.iface, SIGNAL("currentThemeChanged ( QString )"), self.setCurrentTheme)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu( QCoreApplication.translate( "REL",
            "&Remove empty layers" ),self.action ) 
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        numLayers = 0
        self.iface.mapCanvas().setRenderFlag( False ) 
        for layer in self.iface.legendInterface().layers():
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.featureCount() == 0:
                    if QGis.QGIS_VERSION[0:3] < "1.7":
                        QgsMapLayerRegistry.instance().removeMapLayer( layer.getLayerID() )
                    else: 
                        QgsMapLayerRegistry.instance().removeMapLayer( layer.id() )
                    numLayers += 1

        msg = ''
        if numLayers == 0:
            msg = QCoreApplication.translate( "REL", 'There are no empty layers to remove.' )
        elif numLayers == 1: 
            msg = QCoreApplication.translate( "REL", 'There has been removed 1 layer.' )
        else:
            msg = QCoreApplication.translate( "REL", 'There have been removed ' ) + \
                str( numLayers ) + QCoreApplication.translate( "REL", ' layers.' ) 
      
        QMessageBox.information( self.iface.mainWindow(), QCoreApplication.translate( "REL", 
              "Remove empty layers" ), msg, QMessageBox.Ok )

        self.iface.mapCanvas().setRenderFlag( True ) 

    def setCurrentTheme( self, themeName ):
        # Update the icon to match the current theme
        self.action.setIcon( self.getThemeIcon( themeName ) )

    def getThemeIcon( self, themeName="" ):
        # Get the icon from the current theme
        if themeName == "" : themeName = QgsApplication.activeThemePath().split("/")[3]
        if themeName == "newgis": themeName = "gis"
        if themeName == "classic": themeName = "default"
        iconPath = ":/plugins/removeemptylayers/icon_" + themeName + ".png"
        if QFile.exists( iconPath ):
            return QIcon( iconPath )
        if QFile.exists( ":/plugins/removeemptylayers/icon_gis.png" ):
            return QIcon( ":/plugins/removeemptylayers/icon_gis.png" )
        else:
            return QIcon()

    def installTranslator( self ):
        userPluginPath = os.path.join( os.path.dirname( str( QgsApplication.qgisUserDbFilePath() ) ), "python/plugins/RemoveEmptyLayers" )
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
