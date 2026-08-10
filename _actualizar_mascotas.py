from pathlib import Path
from PIL import Image
import re

root = Path(r"D:\Downloads\Proyecto Web\mi-puesto-bazar")
assets = root / "assets" / "img" / "don-perrote"

sources = {
    "ejecutivo": "Gemini_Generated_Image_uo7xl3uo7xl3uo7x.png",
    "leyendo-periodico": "Gemini_Generated_Image_kn3ibgkn3ibgkn3i.png",
    "intelectual-lentes": "Gemini_Generated_Image_iknflgiknflgiknf.png",
    "techie-cables": "Gemini_Generated_Image_k8w3qhk8w3qhk8w3.png",
    "tarjetas-ram": "Gemini_Generated_Image_xf31gjxf31gjxf31.png",
    "chef-dulces": "Gemini_Generated_Image_esmvh8esmvh8esmv.png",
    "viajero": "Gemini_Generated_Image_jvcjjajvcjjajvcj.png",
    "numismatica": "Gemini_Generated_Image_l9a0u4l9a0u4l9a0.png",
    "fuerza-1000kg": "Gemini_Generated_Image_m6ws5km6ws5km6ws.png",
    "futbol": "Gemini_Generated_Image_kizwtzkizwtzkizw.png",
}

for name, source_name in sources.items():
    source = assets / source_name
    target = assets / f"don-perrote-{name}.webp"
    with Image.open(source) as image:
        image = image.convert("RGB")
        image.thumbnail((760, 760), Image.Resampling.LANCZOS)
        image.save(target, "WEBP", quality=82, method=6)

assignments = {
    "revistas.html": [
        ("don-perrote-leyendo-periodico.webp", "Don Perrote leyendo el periódico"),
        ("don-perrote-intelectual-lentes.webp", "Don Perrote intelectual revisando el catálogo"),
    ],
    "electronica.html": [
        ("don-perrote-techie-cables.webp", "Don Perrote techie con cables y conectores"),
        ("don-perrote-tarjetas-ram.webp", "Don Perrote con tarjetas y memorias RAM"),
    ],
    "dulces.html": [
        ("don-perrote-chef-dulces.webp", "Don Perrote chef con dulces y mazapanes"),
        ("don-perrote-viajero.webp", "Don Perrote viajero con accesorios"),
    ],
    "cigarros.html": [
        ("don-perrote-ejecutivo.webp", "Don Perrote ejecutivo de traje"),
        ("don-perrote-numismatica.webp", "Don Perrote con artículos de colección"),
    ],
    "ofertas.html": [
        ("don-perrote-fuerza-1000kg.webp", "Don Perrote levantando 1000 kg"),
        ("don-perrote-futbol.webp", "Don Perrote en una jugada de fútbol"),
    ],
}

for filename, images in assignments.items():
    path = root / filename
    html = path.read_text(encoding="utf-8")
    block_match = re.search(r'(<div class="mascot-feature">)(.*?)(</div>\s*</main>)', html, re.S)
    if not block_match:
        raise RuntimeError(f"No se encontró la tarjeta de mascota en {filename}")
    block = block_match.group(2)
    image_index = 0

    def replace_image(match):
        nonlocal_image_index = replace_image.index
        source, alt = images[nonlocal_image_index]
        replace_image.index += 1
        original = match.group(0)
        original = re.sub(r'src="[^"]+"', f'src="assets/img/don-perrote/{source}"', original)
        original = re.sub(r'alt="[^"]*"', f'alt="{alt}"', original)
        return original

    replace_image.index = 0
    updated_block = re.sub(r'<img\b[^>]*>', replace_image, block, count=2)
    if replace_image.index != 2:
        raise RuntimeError(f"No se sustituyeron dos imágenes en {filename}")
    html = html[:block_match.start(2)] + updated_block + html[block_match.end(2):]
    path.write_text(html, encoding="utf-8")

index_path = root / "index.html"
index_html = index_path.read_text(encoding="utf-8")
index_html = index_html.replace(
    'src="assets/img/don-perrote/don-perrote-ejecutivo.webp" alt="Don Perrote ejecutivo de bienvenida"',
    'src="assets/img/carrusel-cabecera/foto6.png" alt="Don Perrote, mascota del bazar"',
)
index_path.write_text(index_html, encoding="utf-8")

print("Diez imágenes WebP preparadas, asignadas a las cinco subpáginas y fotos originales restauradas en inicio.")
