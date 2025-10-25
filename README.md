# โครงงานเว็บแอปบันทึกข้อมูลสุขภาพ
Project’s Name : Health Record Web App
## DEADLINE : 14/10/2025 (Presentation Day)
<img width="630" height="244" alt="image" src="https://github.com/user-attachments/assets/3f077257-3d85-4ab7-9a43-66c90489ebae" />

Docs : https://docs.google.com/document/d/1HewruGs_NsizaV5w6IE_RjJQyBTFMWQQaoSuwaCKA48/edit?tab=t.0

## Template Migration Notes
- Static HTML versions of the EJS views now live under `templates/`.
- Shared layout pieces are available as `{% include %}` targets in `templates/header/head.html`, `templates/partials/nav.html`, and `templates/partials/menu.html`.
- Navigation highlighting expects a `current_path` context variable (e.g. set via a Django view).
- Individual pages are in `templates/pages/` (`symptom.html`, `Medication.html`, `Schedule.html`, `List.html`, `HDV.html`) and keep the original markup/JS for use in Django.
