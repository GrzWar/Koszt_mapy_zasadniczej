# -*- coding: utf-8 -*-
"""
/***************************************************************************
 KosztMapy
                                 A QGIS plugin
 Oblicza prawdopodobny koszt zamawianej mapy zasadniczej
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-12-11
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Grzegorz Warszycki
        email                : opti33@gmail.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QTableWidgetItem
from qgis.core import QgsApplication,QgsMessageLog, Qgis, QgsVectorLayer, QgsProject, QgsMapLayerProxyModel, QgsField, QgsExpressionContext, QgsExpressionContextUtils, QgsExpression
import processing
import os
from .cost_table import DlgCosts

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .koszt_mapy_dialog import KosztMapyDialog


class KosztMapy:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'KosztMapy_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Koszt mapy zasadniczej')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('KosztMapy', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/koszt_mapy/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Koszt mapy zasadniczej'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Koszt mapy zasadniczej'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = KosztMapyDialog()
            self.dlg.cmbLayer.setFilters(QgsMapLayerProxyModel.PolygonLayer)


        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:

            #specyfying the direction of files with voivodeship (included to plugin) and direction of temporary files
            path_voivodeship = str(os.path.join(os.path.dirname(__file__),'PRG','A02_Granice_powiatow_plugin.shp'))
            target_path = str(os.path.join(os.path.dirname(__file__),'PRG','clipped_plugin.shp'))
            #Logs for debugging
            QgsMessageLog.logMessage("source_path: {}".format(path_voivodeship), "koszt_mapy", level=Qgis.Info)
            QgsMessageLog.logMessage("target_path: {}".format(target_path), "koszt_mapy", level=Qgis.Info)

            #loading layer with voivodeships included in plugin package
            vector_voivodeship = QgsVectorLayer(path_voivodeship, "granice_powiatow", "ogr")
            QgsProject.instance().addMapLayer(vector_voivodeship)
            vector_voivodeship.setProviderEncoding(u'UTF-8')
            vector_voivodeship.dataProvider().setEncoding(u'UTF-8')
            #specyfying range of map with the vector layer from combobox
            lyrMapPoly = self.dlg.cmbLayer.currentLayer()
            #clipping layer with voivodeship with the polygon and creating a shapefile in plugin directory
            layer_clip = processing.run('qgis:clip',
                           {'INPUT': vector_voivodeship,
                            'OVERLAY': lyrMapPoly,
                            'OUTPUT': target_path })
            #adding file to the project
            vector_clipped = QgsVectorLayer(target_path, "clipped_plugin", "ogr")
            QgsProject.instance().addMapLayer(vector_clipped)

            #adding area attribute
            clipped_layer_provider = vector_clipped.dataProvider()
            clipped_layer_provider.addAttributes([QgsField("area", QVariant.Double)])
            vector_clipped.updateFields()

            #calculating area
            features = vector_clipped.getFeatures()
            expression1 = QgsExpression('$area')
            context = QgsExpressionContext()
            context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(vector_clipped))
            vector_clipped.startEditing()
            for f in features:
                id = f.id()
                context.setFeature(f)
                f['area'] = expression1.evaluate(context)
                vector_clipped.updateFeature(f)
            vector_clipped.commitChanges()

            #making table with results
            dlgCosts = DlgCosts()
            for feature in vector_clipped.getFeatures():
                row = dlgCosts.tblCosts.rowCount()
                dlgCosts.tblCosts.insertRow(row)
                # assigning the name of the powiat to the row
                dlgCosts.tblCosts.setItem(row, 0, QTableWidgetItem(str(feature["JPT_NAZWA_"])))
                # calculating area in "ha" units
                area_ha = (feature["area"]/10000)
                rounded_area_ha = round((feature["area"]/10000),4)
                dlgCosts.tblCosts.setItem(row, 1, QTableWidgetItem(str(rounded_area_ha)+" ha"))


                # calculating cost of map
                if area_ha < 10:
                    cost_of_map = ((area_ha * 21.53 * 2))
                if area_ha > 10 and area_ha < 100:
                    cost_of_map = ((((21.53 * 10) +((area_ha-10)*21.53 * 0.8))*2))
                if area_ha > 100:
                    cost_of_map = ((((10 + 21.53 +(90*21.53*0.8)+((area_ha-100)*21.53 * 0.6))*2)))

                # calculating cost for 1:500 scale
                cost_of_map_500 = cost_of_map * 1
                # calculating cost for 1:1000 scale
                cost_of_map_1000 = cost_of_map * 0.8
                # calculating cost for 1:2000 scale
                cost_of_map_2000 = cost_of_map * 0.5
                # calculating cost for 1:5000 scale
                cost_of_map_5000 = cost_of_map * 0.3

                #populating table with costs
                dlgCosts.tblCosts.setItem(row, 2, QTableWidgetItem(str(round(cost_of_map_500,2))+" zł"))
                dlgCosts.tblCosts.setItem(row, 3, QTableWidgetItem(str(round(cost_of_map_1000, 2)) + " zł"))
                dlgCosts.tblCosts.setItem(row, 4, QTableWidgetItem(str(round(cost_of_map_2000, 2)) + " zł"))
                dlgCosts.tblCosts.setItem(row, 5, QTableWidgetItem(str(round(cost_of_map_5000, 2)) + " zł"))



            dlgCosts.show()
            dlgCosts.exec_()

            #removing layers from QGIS
            QgsProject.instance().removeMapLayer(vector_clipped)
            QgsProject.instance().removeMapLayer(vector_voivodeship)

            # deleting files created during the plugin processing
            os.remove(str(os.path.join(os.path.dirname(__file__),"PRG","clipped_plugin.shp")))
            os.remove(str(os.path.join(os.path.dirname(__file__),"PRG","clipped_plugin.dbf")))
            os.remove(str(os.path.join(os.path.dirname(__file__),"PRG","clipped_plugin.prj")))
            os.remove(str(os.path.join(os.path.dirname(__file__),"PRG","clipped_plugin.shx")))

            #refreshing canvas

            self.iface.mapCanvas().refresh()

            pass