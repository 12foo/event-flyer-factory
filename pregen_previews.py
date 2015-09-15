#!/usr/bin/env python3
# pregen_previews.py -- pregenerates all previews that don't yet exist.

import pdf_builder, layouts

print("Generating previews...")
for template in pdf_builder.templates:
    for layout_name, layout in layouts.layouts().items():
        print("- generated " + pdf_builder.get_preview(template, layout_name))
