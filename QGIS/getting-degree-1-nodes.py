layer = iface.activeLayer()
crs = "EPSG:2285" 

point_layer = QgsVectorLayer(f"Point?crs={crs}", "End Points", "memory")
provider = point_layer.dataProvider()

features = []
for feature in layer.getFeatures():
    geom = feature.geometry()
    if geom.type() == QgsWkbTypes.LineGeometry:
        if geom.isMultipart():
            lines = geom.asMultiPolyline()
        else:
            lines = [geom.asPolyline()]
        
        for line in lines:
            if line:
                start_feat = QgsFeature()
                start_feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(line[0])))
                features.append(start_feat)
                if line[0] != line[-1]:
                    end_feat = QgsFeature()
                    end_feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(line[-1])))
                    features.append(end_feat)

provider.addFeatures(features)
point_layer.updateExtents()

if not features:
    print("No endpoints were added. Please check your input layer.")
else:
    QgsProject.instance().addMapLayer(point_layer)
