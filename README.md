# Autobanker  
Maya script to create a control with banking attributes based on geometry's vertices. [Watch a video explanation](https://youtu.be/k9aUU8taqxo), or read below.  
[![VIDEO](https://media.giphy.com/media/pxokOz05QhoT9er2ui/giphy.gif)](https://youtu.be/k9aUU8taqxo "Autobanker")

Note: Script only works with Y-up axis.

To use:  
1. Place autoBanker.py in a maya scripts directory.
2. Select the geometry you would like to bank.
3. In python, run:
```
import autoBanker
autoBanker.create()
```

A control should be made with two attributes, "Bank Sideways", and "Bank Forwards", playing with the values of these attributes should move the geometry based on the lowest pivots.
