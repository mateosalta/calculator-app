import QtQuick 2.3
import Ubuntu.Components 1.1

Grid {
    id: root
    columns: 4

    property var model: null

    property real buttonRatio: 1

    Component.onCompleted: {
        buildModel();
    }
    onModelChanged: {
        buildModel();
    }

    function buildModel() {
        generatedModel.clear();

        var emptyPlaces = new Array();

        for (var i = 0; i < root.model.length; i++) {
            var entry = root.model[i];
            var text = entry.number || entry.forceNumber ? Number(entry.number).toLocaleString(Qt.locale(), "f", 0) : entry.text ? entry.text : "";
            generatedModel.append(
                        {
                            text: text,
                            wFactor: entry.wFactor ? entry.wFactor : 1,
                            hFactor: entry.hFactor ? entry.hFactor : 1,
                            action: entry.action ? entry.action : "push",
                            objectName: entry.objectName ? entry.objectName: "",
                            pushText: entry.pushText ? entry.pushText : text
                        }
                    )

            if (entry.wFactor && entry.wFactor > 1) {
                for (var j = 1; j < entry.wFactor; j++) {
                    generatedModel.append({text: ""})
                }
                for (var j = 0; j < emptyPlaces.length; j++) {
                    emptyPlaces[j] = emptyPlaces[j] - entry.wFactor + 1;
                }
            }

            if (entry.hFactor && entry.hFactor > 1) {
                for (var j = 1; j < entry.hFactor; j++) {
                    emptyPlaces.push(i + columns * j);
                }
            }
            if (i+1 === emptyPlaces[0]) {
                generatedModel.append({text: ""})
                emptyPlaces = emptyPlaces.splice(1, emptyPlaces.length);
            }
        }
    }


    Repeater {
        id: repeater
        model: ListModel {
            id: generatedModel
        }

        Loader {
            sourceComponent: model.text ? buttonComponent : undefined

            height: width * root.buttonRatio
            width: root.width / root.columns - root.spacing

            Component {
                id: buttonComponent

                Item {
                    KeyboardButton {
                        height: keyboardsRow.baseSize * root.buttonRatio * model.hFactor + (root.spacing * (model.hFactor - 1))
                        width: keyboardsRow.baseSize * model.wFactor + (root.spacing * (model.wFactor - 1))
                        text: model.text
                        objectName: model.objectName
                        onClicked: {
                            print("invoking:")
                            switch (model.action) {
                            case "push":
                                formulaPush(model.pushText);
                                break;
                            case "delete":
                                deleteLastFormulaElement();
                                break;
                            case "changeSign":
                                // TODO: Implement changeSign() function
                                //changeSign()
                                break;
                            case "calculate":
                                calculate();
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
}
