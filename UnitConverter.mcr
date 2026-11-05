macroScript UnitConverter
category:"H MEDIA 3D ACADEMY"
tooltip:"Measure & Convert"
buttonText:"Unit Converter"
iconName:"HMedia3D/tape"
autoUndoEnabled:false
(
    on execute do
    (
        python.ExecuteFile ((getDir #userScripts) + "\\HMediaUnitConverter\\launch.py")
    )
)
