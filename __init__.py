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
 This script initializes the plugin, making it known to QGIS.
"""
from PyQt4.QtCore import QCoreApplication

def name():
    return QCoreApplication.translate( "REL", "Remove empty layers from the map" )
def description():
    return QCoreApplication.translate( "REL", "'Cleans' the layer list widget (legend) by removing empty layers" )
def version():
    return "Version 2.0"
def icon():
    return "icon_default.png"
def qgisMinimumVersion():
    return "2.0"
def classFactory(iface):
    # load RemoveEmptyLayers class from file RemoveEmptyLayers
    from removeemptylayers import RemoveEmptyLayers
    return RemoveEmptyLayers(iface)
