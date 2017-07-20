(TeX-add-style-hook
 "euler"
 (lambda ()
   (TeX-run-style-hooks
    "latex2e"
    "standalone"
    "standalone10"
    "amsmath"
    "amsthm"
    "pgfplots"
    "tikz"))
 :latex)

