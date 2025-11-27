# Universal Camo Gen

Universal Camo Gen is a Python-based procedural generation tool designed to create high-resolution military camouflage patterns. It utilizes advanced noise algorithms, domain warping, and wave interference mathematics to replicate iconic patterns such as Tiger Stripe, M81 Woodland, and Kryptek-style hexagon grids.

The application features a complete Graphical User Interface (GUI) built with Tkinter, allowing for real-time parameter adjustment, color customization, and layer control.

## Features

* **9 Procedural Pattern Engines:** Distinct algorithms tailored to replicate specific camouflage families (Organic, Brushstroke, Dithering, and Geometric).
* **Real-Time Customization:** Adjust scale, distortion, flow, and edge roughness instantly.
* **Layer Management:** Toggle individual color layers on or off to create simplified patterns or isolate specific shapes.
* **Density Control:** Precise 1-9 integer scaling for layer coverage thresholds.
* **Digital Mode:** Post-processing filter to pixelate any pattern into a "MARPAT/CADPAT" style digital block pattern.
* **Color Tools:** Full palette customization with hexadecimal color pickers, individual slot randomizers, and a full palette shuffler.
* **High-Resolution Export:** Save generated patterns as PNG files.

## Supported Patterns

1.  **Tiger Stripe Inspired:** Anisotropic sine wave distortion with "pinching" logic to create tapered shards.
2.  **M81 Woodland Inspired:** Isotropic domain warping creating large, interlocking organic blobs.
3.  **Flecktarn Inspired:** Dual-frequency noise generation simulating clustered pointillism/dithering.
4.  **Chocolate Chip Inspired:** Six-color desert logic with background blobs and high-frequency "rock" overlays.
5.  **British DPM Inspired:** Swirling distortion with stippled edge noise to simulate the "hairy" look of Disruptive Pattern Material.
6.  **British Brush Stroke Inspired:** Low-frequency sweeping shapes multiplied by high-frequency bristle textures.
7.  **Lizard Inspired:** Horizontal "dry brush" logic creating broken, trailing organic lines.
8.  **Puzzle Inspired:** Hard-edged cellular noise creating "jigsaw" style shapes (e.g., Belgium Jigsaw).
9.  **Kryptek Inspired:** Geometric engine using 3-axis triangle wave interference to generate interconnected hexagonal webs.

## Installation

### Prerequisites
* Python 3.x installed on your system.

### Dependencies
This application requires `numpy` for vectorized math operations and `Pillow` (PIL) for image processing and rendering.

1.  Clone or download this repository.
2.  Open your terminal or command prompt.
3.  Install the required libraries:

```bash
pip install numpy pillow
```

## Usage

1.  Navigate to the directory containing the script.
2.  Run the application:

```bash
python camo_gen.py
```

3.  **Pattern Selection:** Use the dropdown menu at the top to select the desired camouflage engine.
4.  **Geometry Settings:**
    * **Scale:** Controls the zoom level of the pattern (5 = dense, 1000 = massive).
    * **Distortion:** Controls the amount of liquid warping applied to the shapes.
    * **Feat A / Feat B:** Context-sensitive sliders that change function based on the selected pattern (e.g., Horizontal Stretch, Dot Size, Line Thickness).
5.  **Layer Density:** Adjust sliders 1 through 9 to control how much of the canvas is covered by Layer 1, 2, and 3 respectively.
6.  **Colors:** Click the colored boxes to change the palette. Click the "Die" icon to randomize a single color. Click "Shuffle Colors" to swap the existing palette order.
7.  **Save:** Click "Save Image" to export the current view to a PNG file.

## Technical Implementation

The application avoids using heavy external noise libraries (like `libnoise`) by implementing vectorized noise generation using NumPy.

* **Noise Generation:** It generates a low-resolution grid of random values and scales it up using Bicubic interpolation to create smooth gradient noise.
* **Domain Warping:** It applies secondary noise layers to the coordinate system ($x, y$) before calculating the pattern, resulting in organic, non-linear shapes.
* **Wave Interference:** For geometric patterns, it calculates the interference of triangle waves rotated at 0, 60, and 120 degrees to form hexagonal lattices mathematically.

## License

This project is provided as open source software. You are free to use, modify, and distribute it as needed.
