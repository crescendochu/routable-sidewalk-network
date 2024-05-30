layer = iface.activeLayer()
crs = "EPSG:2285"

# Create the point layer with an additional attribute for counting
point_layer = QgsVectorLayer(f"Point?crs={crs}", "degree-1-nodes", "memory")
provider = point_layer.dataProvider()
provider.addAttributes([QgsField("count", QVariant.Int)])
point_layer.updateFields()

# Dictionary to keep track of points and their counts
point_dict = {}

for feature in layer.getFeatures():
    geom = feature.geometry()
    if geom.type() == QgsWkbTypes.LineGeometry:
        if geom.isMultipart():
            lines = geom.asMultiPolyline()
        else:
            lines = [geom.asPolyline()]
        
        for line in lines:
            if line:
                # Process start point
                start_point = QgsPointXY(line[0])
                start_key = (start_point.x(), start_point.y())
                point_dict[start_key] = point_dict.get(start_key, 0) + 1
                
                # Process end point if different from start
                if line[0] != line[-1]:
                    end_point = QgsPointXY(line[-1])
                    end_key = (end_point.x(), end_point.y())
                    point_dict[end_key] = point_dict.get(end_key, 0) + 1

# Add points with count = 1 from the dictionary to the layer
features = []
for key, count in point_dict.items():
    if count == 1:
        feat = QgsFeature()
        point = QgsPointXY(key[0], key[1])
        feat.setGeometry(QgsGeometry.fromPointXY(point))
        feat.setAttributes([count])
        features.append(feat)

provider.addFeatures(features)
point_layer.updateExtents()

if not features:
    print("No degree 1 endpoints were added. Please check your input layer.")
else:
    QgsProject.instance().addMapLayer(point_layer)
