(TeX-add-style-hook
 "centroid"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("standalone" "tikz" "border=5pt")))
   (TeX-run-style-hooks
    "latex2e"
    "standalone"
    "standalone10"
    "tikz"
    "pgfplots"
    "pst-eucl"
    "tkz-euclide"))
 :latex)

