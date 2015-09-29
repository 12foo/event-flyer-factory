#!/usr/bin/env python3
# pregen_previews.py -- pregenerates all previews that don't yet exist.

import pdf_builder, templates

print("Generating previews...")
for template_name, template in templates.templates().items():
    for layout in template.layouts:
        print("- generated " + pdf_builder.get_preview(template_name, layout.__name__))
