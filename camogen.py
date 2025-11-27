import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
from PIL import Image, ImageTk
import numpy as np
import random

class UniversalCamoGen:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Camo Studio v11.0 (Geometric Wave Engine)")
        self.root.geometry("1280x950")
        
        self.width = 900
        self.height = 700
        
        # --- PRESETS ---
        self.defaults = {
            "Tiger Stripe Inspired": {
                "colors": {"base": "#C3B091", "layer1": "#384A20", "layer2": "#6F4E37", "layer3": "#101010"},
                "params": {"scale": 7.0, "distortion": 80.0, "feat_a": 15.0, "feat_b": 2.0, 
                           "thresh1": 3, "thresh2": 5, "thresh3": 3}
            },
            "M81 Woodland Inspired": {
                "colors": {"base": "#B0A182", "layer1": "#3F4533", "layer2": "#4A3224", "layer3": "#121212"},
                "params": {"scale": 10.0, "distortion": 120.0, "feat_a": 7.0, "feat_b": 1.0, 
                           "thresh1": 6, "thresh2": 4, "thresh3": 2}
            },
            "Flecktarn Inspired": {
                "colors": {"base": "#586243", "layer1": "#6D5F44", "layer2": "#3B422E", "layer3": "#181A16"},
                "params": {"scale": 15.0, "distortion": 66.0, "feat_a": 13.0, "feat_b": 25.0, 
                           "thresh1": 5, "thresh2": 3, "thresh3": 1}
            },
            "Chocolate Chip Inspired": { 
                "colors": {"base": "#FFFFFF", "layer1": "#8B4513", "layer2": "#000000", "layer3": "#D2B48C"},
                "params": {"scale": 60.0, "distortion": 0.0, "feat_a": 1.0, "feat_b": 0.0, 
                           "thresh1": 6, "thresh2": 5, "thresh3": 1}
            },
            "British DPM Inspired": { 
                "colors": {"base": "#C8B682", "layer1": "#575E40", "layer2": "#6F482F", "layer3": "#151515"},
                "params": {"scale": 25.0, "distortion": 22.0, "feat_a": 0.0, "feat_b": 1.1, 
                           "thresh1": 4, "thresh2": 4, "thresh3": 1}
            },
            "British Brush Stroke Inspired": { 
                "colors": {"base": "#E0D6AA", "layer1": "#788055", "layer2": "#8B4513", "layer3": "#402518"},
                "params": {"scale": 25.0, "distortion": 40.0, "feat_a": 10.0, "feat_b": 25.0, 
                           "thresh1": 6, "thresh2": 5, "thresh3": 4}
            },
            "Lizard Inspired": { 
                "colors": {"base": "#E2D3A7", "layer1": "#4B5F3E", "layer2": "#8C583A", "layer3": "#3E4435"},
                "params": {"scale": 20.0, "distortion": 30.0, "feat_a": 12.0, "feat_b": 35.0, 
                           "thresh1": 6, "thresh2": 5, "thresh3": 2}
            },
            "Puzzle Inspired": { 
                "colors": {"base": "#D8CBA0", "layer1": "#607045", "layer2": "#805040", "layer3": "#202020"},
                "params": {"scale": 35.0, "distortion": 10.0, "feat_a": 1.0, "feat_b": 0.0, 
                           "thresh1": 7, "thresh2": 6, "thresh3": 5}
            },
            "Kryptek Inspired": { 
                "colors": {"base": "#2b2b2b", "layer1": "#4B5320", "layer2": "#707850", "layer3": "#050505"},
                # Defaults: Scale 100, Distortion 200, Feat A 0, Feat B 50
                "params": {"scale": 100.0, "distortion": 200.0, "feat_a": 6.0, "feat_b": 0.0, 
                           "thresh1": 5, "thresh2": 5, "thresh3": 5}
            }
        }
        
        self.current_mode = tk.StringVar(value="Kryptek Inspired")
        self.colors = self.defaults["Kryptek Inspired"]["colors"].copy()
        
        self.vars = {} 
        self.val_labels = {}
        self.layer_vars = {} 
        self.digital_mode = tk.BooleanVar(value=False)

        # --- UI LAYOUT ---
        self.control_frame = ttk.Frame(root, padding="20")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.canvas_frame = ttk.Frame(root, padding="10", relief="sunken")
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas_label = ttk.Label(self.canvas_frame)
        self.canvas_label.pack(expand=True)

        self.setup_controls()
        
    def setup_controls(self):
        ttk.Label(self.control_frame, text="Pattern Type", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        
        mode_frame = ttk.Frame(self.control_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        mode_cb = ttk.Combobox(mode_frame, textvariable=self.current_mode, 
                               values=list(self.defaults.keys()), state="readonly", width=18)
        mode_cb.pack(side=tk.LEFT, fill=tk.X, expand=True)
        mode_cb.bind("<<ComboboxSelected>>", self.on_mode_change)
        
        btn_reset = ttk.Button(mode_frame, text="↺ Defaults", width=10, command=self.reset_to_defaults)
        btn_reset.pack(side=tk.RIGHT, padx=(5,0))

        chk = ttk.Checkbutton(self.control_frame, text="Digital / Pixelated Mode", 
                              variable=self.digital_mode, command=self.update_req)
        chk.pack(fill=tk.X, pady=(0, 15))

        # Sliders
        ttk.Label(self.control_frame, text="Geometry Settings", font=("Segoe UI", 10, "bold")).pack(pady=(5,5), anchor="w")
        # Scale updated to 1000.0
        self.add_slider("Scale (Zoom)", 5.0, 1000.0, "scale")
        self.add_slider("Distortion", 0.0, 200.0, "distortion")
        self.add_slider("Feat A (Stretch/Flow)", 0.0, 30.0, "feat_a")
        self.add_slider("Feat B (Edge/Rough)", 0.0, 50.0, "feat_b")
        
        ttk.Separator(self.control_frame, orient='horizontal').pack(fill='x', pady=15)
        
        ttk.Label(self.control_frame, text="Layer Density (1-9)", font=("Segoe UI", 10, "bold")).pack(pady=(0,5), anchor="w")
        self.add_slider("Layer 1 Density", 1, 9, "thresh1", is_int=True)
        self.add_slider("Layer 2 Density", 1, 9, "thresh2", is_int=True)
        self.add_slider("Layer 3 Density", 1, 9, "thresh3", is_int=True)

        ttk.Separator(self.control_frame, orient='horizontal').pack(fill='x', pady=15)

        ttk.Label(self.control_frame, text="Palette & Layers", font=("Segoe UI", 10, "bold")).pack(pady=(0,5), anchor="w")
        
        self.color_btns = {}
        for role in ["base", "layer1", "layer2", "layer3"]:
            row = ttk.Frame(self.control_frame)
            row.pack(fill=tk.X, pady=2)
            
            if role != "base":
                var = tk.BooleanVar(value=True)
                self.layer_vars[role] = var
                chk = ttk.Checkbutton(row, variable=var, command=self.update_req)
                chk.pack(side=tk.LEFT)
            else:
                ttk.Frame(row, width=24).pack(side=tk.LEFT)
                
            ttk.Label(row, text=role.title(), width=10).pack(side=tk.LEFT)
            
            picker_btn = tk.Button(row, bg=self.colors[role], width=6, 
                            command=lambda r=role: self.pick_color(r))
            picker_btn.pack(side=tk.RIGHT, padx=2)
            self.color_btns[role] = picker_btn

            rand_btn = ttk.Button(row, text="🎲", width=3, 
                                  command=lambda r=role: self.randomize_single_color(r))
            rand_btn.pack(side=tk.RIGHT, padx=2)

        shuffle_btn = ttk.Button(self.control_frame, text="🔀 Shuffle Colors", command=self.shuffle_colors)
        shuffle_btn.pack(fill=tk.X, pady=(10, 5))

        ttk.Separator(self.control_frame, orient='horizontal').pack(fill='x', pady=15)
        
        ttk.Button(self.control_frame, text="Regenerate Seed", command=self.new_seed).pack(fill=tk.X, pady=5)
        ttk.Button(self.control_frame, text="Save Image", command=self.save_image).pack(fill=tk.X, pady=5)

        self.apply_defaults(self.current_mode.get())

    def add_slider(self, label_text, min_v, max_v, attr_name, is_int=False):
        header_frame = ttk.Frame(self.control_frame)
        header_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(header_frame, text=label_text).pack(side=tk.LEFT)
        
        start_val = min_v
        if is_int:
            display_text = f"{int(start_val)}"
        else:
            display_text = f"{start_val:.1f}"

        val_label = ttk.Label(header_frame, text=display_text, foreground="#555")
        val_label.pack(side=tk.RIGHT)
        self.val_labels[attr_name] = val_label
        
        var = tk.DoubleVar(value=start_val)
        self.vars[attr_name] = var
        
        def on_slide(val):
            val_float = float(val)
            if is_int:
                snapped = round(val_float)
                self.val_labels[attr_name].config(text=f"{snapped}")
            else:
                self.val_labels[attr_name].config(text=f"{val_float:.1f}")
            self.update_req()

        scale = ttk.Scale(self.control_frame, from_=min_v, to=max_v, variable=var, command=on_slide)
        scale.pack(fill=tk.X, pady=(0, 5))

    def apply_defaults(self, mode):
        params = self.defaults[mode]["params"]
        self.suppress_updates = True
        
        for key, val in params.items():
            if key in self.vars:
                self.vars[key].set(val)
                if "thresh" in key:
                     self.val_labels[key].config(text=f"{int(val)}")
                else:
                     self.val_labels[key].config(text=f"{val:.1f}")
        
        for var in self.layer_vars.values():
            var.set(True)

        self.suppress_updates = False
        self.generate_pattern()

    def reset_to_defaults(self):
        mode = self.current_mode.get()
        self.colors = self.defaults[mode]["colors"].copy()
        for role, btn in self.color_btns.items():
            btn.config(bg=self.colors[role])
        self.apply_defaults(mode)

    def on_mode_change(self, event):
        self.reset_to_defaults()

    def update_req(self):
        if getattr(self, "suppress_updates", False): return
        self.generate_pattern()
        
    def new_seed(self):
        if not hasattr(self, 'seed_offset'): self.seed_offset = 0
        self.seed_offset += 1
        self.generate_pattern()

    def pick_color(self, role):
        c = colorchooser.askcolor(color=self.colors[role])[1]
        if c:
            self.colors[role] = c
            self.color_btns[role].config(bg=c)
            self.generate_pattern()

    def randomize_single_color(self, role):
        r = lambda: random.randint(0, 255)
        color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
        self.colors[role] = color
        self.color_btns[role].config(bg=color)
        self.generate_pattern()

    def shuffle_colors(self):
        keys = list(self.colors.keys()) 
        values = list(self.colors.values())
        random.shuffle(values)
        for i, key in enumerate(keys):
            self.colors[key] = values[i]
            self.color_btns[key].config(bg=values[i])
        self.generate_pattern()

    def get_noise(self, h, w, scale, stretch_x=1.0, stretch_y=1.0, seed_add=0):
        seed_base = int(self.vars['scale'].get()) + seed_add + getattr(self, 'seed_offset', 0)
        np.random.seed(seed_base)
        safe_scale = max(1.0, scale)
        gh = int(h / (safe_scale * stretch_y)) + 2 
        gw = int(w / (safe_scale * stretch_x)) + 2
        noise = np.random.rand(gh, gw)
        img = Image.fromarray((noise * 255).astype(np.uint8))
        img = img.resize((w, h), resample=Image.BICUBIC)
        return np.array(img).astype(np.float64) / 255.0

    def generate_pattern(self):
        mode = self.current_mode.get()
        w, h = self.width, self.height
        
        scale = self.vars['scale'].get()
        dist = self.vars['distortion'].get()
        feat_a = self.vars['feat_a'].get()
        feat_b = self.vars['feat_b'].get()
        
        d1 = round(self.vars['thresh1'].get())
        d2 = round(self.vars['thresh2'].get())
        d3 = round(self.vars['thresh3'].get())
        
        def get_cutoff(density_int): return 1.0 - (density_int / 10.0)
        t1 = get_cutoff(d1)
        t2 = get_cutoff(d2)
        t3 = get_cutoff(d3)

        final = np.zeros((h, w, 3), dtype=np.uint8)
        hex2rgb = lambda x: tuple(int(x[i:i+2], 16) for i in (1, 3, 5))
        final[:,:] = hex2rgb(self.colors["base"])

        if mode == "Kryptek Inspired":
            self.algo_kryptek_v11(final, w, h, scale, dist, feat_a, feat_b, hex2rgb, t1, t2, t3)
        elif mode == "Tiger Stripe Inspired":
            self.algo_tiger(final, w, h, scale, dist, feat_a, feat_b, hex2rgb, t1, t2, t3)
        elif mode in ["M81 Woodland Inspired", "Puzzle Inspired"]:
            self.algo_woodland_family(final, w, h, scale, dist, feat_a, feat_b, hex2rgb, t1, t2, t3)
        elif mode == "British DPM Inspired":
            self.algo_dpm(final, w, h, scale, dist, feat_a, feat_b, hex2rgb, t1, t2, t3)
        elif mode == "Flecktarn Inspired":
            self.algo_flecktarn(final, w, h, scale, dist, feat_a, feat_b, hex2rgb, t1, t2, t3)
        elif mode == "Chocolate Chip Inspired":
            self.algo_chocolate(final, w, h, scale, dist, feat_a, feat_b, hex2rgb, t1, t2, t3)
        elif mode == "British Brush Stroke Inspired":
            self.algo_brush_v2(final, w, h, scale, dist, feat_a, feat_b, hex2rgb, t1, t2, t3)
        elif "Lizard" in mode:
            self.algo_lizard_v2(final, w, h, scale, dist, feat_a, feat_b, hex2rgb, t1, t2, t3)

        img = Image.fromarray(final)
        if self.digital_mode.get():
            block_size = 8
            small = img.resize((w // block_size, h // block_size), resample=Image.NEAREST)
            img = small.resize((w, h), resample=Image.NEAREST)

        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas_label.configure(image=self.tk_img)

    # --- ALGORITHM: KRYPTEK V11 (TRIANGLE WAVE) ---
    def algo_kryptek_v11(self, final, w, h, scale, dist, fade_amt, line_thick, hex2rgb, t1, t2, t3):
        bg_noise = self.get_noise(h, w, scale * 3.0, seed_add=100)
        x = np.linspace(0, w, w).reshape(1, w)
        y = np.linspace(0, h, h).reshape(h, 1)
        
        warp = self.get_noise(h, w, scale * 4.0, seed_add=200) * dist
        x_dist = x + warp
        y_dist = y + warp
        freq = scale / 500.0
        
        # TRIANGLE WAVE FUNCTION: Creates linear gradients (straight lines)
        # Standard Cosine creates curved gradients (circles).
        def tri(t):
            # Maps periodic input to -1.0 ... 1.0 in a linear zig-zag
            return np.abs((t / np.pi) % 2.0 - 1.0) * 2.0 - 1.0

        # 3-Axis Triangle Wave Interference
        v1 = tri(x_dist * freq)
        v2 = tri(x_dist * freq * -0.5 + y_dist * freq * 0.866)
        v3 = tri(x_dist * freq * -0.5 - y_dist * freq * 0.866)
        
        # Sum them up
        # The interference of linear gradients creates polygonal shapes.
        raw_hex = v1 + v2 + v3
        
        # Normalize (roughly -3 to +3 -> 0 to 1)
        raw_hex = (raw_hex + 3.0) / 6.0

        # CELL LOGIC (Peaks)
        cell_thresh = 0.4 + (line_thick / 50.0) * 0.4
        cell_mask = (raw_hex > cell_thresh)
        web_mask = ~cell_mask
        
        fade_mask_noise = self.get_noise(h, w, scale * 4.0, seed_add=555)
        fade_cutoff = fade_amt / 40.0
        visible_mask = fade_mask_noise > fade_cutoff
        final_grid = web_mask & visible_mask
        
        offset = 15 
        shadow_grid = np.roll(final_grid, offset, axis=0)
        shadow_grid = np.roll(shadow_grid, offset, axis=1)
        
        if self.layer_vars['layer1'].get():
            final[bg_noise > 0.5] = hex2rgb(self.colors["layer1"])
        if self.layer_vars['layer3'].get():
            final[shadow_grid] = hex2rgb(self.colors["layer3"])
        if self.layer_vars['layer2'].get():
            final[final_grid] = hex2rgb(self.colors["layer2"])

    def algo_lizard_v2(self, final, w, h, scale, dist, stretch, breakage, hex2rgb, t1, t2, t3):
        base_stretch = max(1.0, stretch / 2.0)
        blobs = self.get_noise(h, w, scale, stretch_x=base_stretch, seed_add=100)
        scratch_scale = max(1.0, scale / 4.0)
        scratch_stretch = max(5.0, stretch * 2.0)
        scratches = self.get_noise(h, w, scratch_scale, stretch_x=scratch_stretch, seed_add=200)
        warp = self.get_noise(h, w, scale * 2.0, seed_add=300) * (dist / 100.0)
        lizard_map = (blobs * (0.3 + 0.7 * scratches)) + warp
        if self.layer_vars['layer1'].get(): final[lizard_map > t1] = hex2rgb(self.colors["layer1"])
        if self.layer_vars['layer2'].get(): final[lizard_map > (t2 + 0.1)] = hex2rgb(self.colors["layer2"])
        if self.layer_vars['layer3'].get(): 
            l3_map = lizard_map * scratches
            final[l3_map > (t3 + 0.15)] = hex2rgb(self.colors["layer3"])

    def algo_brush_v2(self, final, w, h, scale, dist, stretch, bristle_tex, hex2rgb, t1, t2, t3):
        stroke_scale = scale * 2.0
        stroke_stretch = max(4.0, stretch + 2.0)
        strokes_1 = self.get_noise(h, w, stroke_scale, stretch_x=stroke_stretch, seed_add=10)
        strokes_2 = self.get_noise(h, w, stroke_scale, stretch_x=stroke_stretch, seed_add=20)
        strokes_3 = self.get_noise(h, w, stroke_scale, stretch_x=stroke_stretch, seed_add=30)
        bristle_scale = max(1.0, scale / 5.0)
        bristles = self.get_noise(h, w, bristle_scale, stretch_x=stroke_stretch*1.5, seed_add=99)
        bristle_mix = bristle_tex / 50.0 
        texture_mask = (1.0 - bristle_mix) + (bristles * bristle_mix)
        warp = self.get_noise(h, w, scale * 3.0, seed_add=500) * (dist / 150.0)
        s1_final = (strokes_1 * texture_mask) + warp
        s2_final = (strokes_2 * texture_mask) + warp
        s3_final = (strokes_3 * texture_mask) + warp
        if self.layer_vars['layer1'].get(): final[s1_final > t1] = hex2rgb(self.colors["layer1"])
        if self.layer_vars['layer2'].get(): final[s2_final > t2] = hex2rgb(self.colors["layer2"])
        if self.layer_vars['layer3'].get(): final[s3_final > t3] = hex2rgb(self.colors["layer3"])

    def algo_tiger(self, final, w, h, scale, dist, stretch, jagged, hex2rgb, t1, t2, t3):
        y_grid = np.linspace(0, h, h).reshape(h, 1)
        micro_noise = np.random.rand(h, w) * jagged
        flow_map = self.get_noise(h, w, scale*2, stretch_x=stretch, seed_add=10)
        distorted_y = y_grid + micro_noise + (flow_map * dist)
        freq = scale / 250.0
        if self.layer_vars['layer1'].get():
            pinch1 = self.get_noise(h, w, scale, stretch_x=stretch/2, seed_add=20)
            wave1 = np.sin(distorted_y * freq) * (1 + 1.2 * (pinch1 - 0.5))
            final[wave1 > t1] = hex2rgb(self.colors["layer1"])
        if self.layer_vars['layer2'].get() or self.layer_vars['layer3'].get():
            pinch2 = self.get_noise(h, w, scale, stretch_x=stretch, seed_add=30)
            wave2 = np.sin(distorted_y * (freq * 1.2) + 1.0) * (1 + 1.2 * (pinch2 - 0.5))
            if self.layer_vars['layer2'].get(): final[wave2 > t2] = hex2rgb(self.colors["layer2"])
            if self.layer_vars['layer3'].get(): final[wave2 > (t3 + 0.15)] = hex2rgb(self.colors["layer3"])

    def algo_dpm(self, final, w, h, scale, dist, stretch, rough, hex2rgb, t1, t2, t3):
        warp_x = self.get_noise(h, w, scale * 3, seed_add=50) * dist
        stipple = self.get_noise(h, w, 3.0, seed_add=777) * (rough / 15.0)
        base_scale = scale * 2.0
        n1 = self.get_noise(h, w, base_scale, seed_add=100) + warp_x * 0.01 + stipple
        n2 = self.get_noise(h, w, base_scale, seed_add=200) + warp_x * 0.01 + stipple
        n3 = self.get_noise(h, w, base_scale, seed_add=300) + warp_x * 0.01 + stipple
        if self.layer_vars['layer1'].get(): final[n1 > t1] = hex2rgb(self.colors["layer1"])
        if self.layer_vars['layer2'].get(): final[n2 > t2] = hex2rgb(self.colors["layer2"])
        if self.layer_vars['layer3'].get(): final[n3 > t3] = hex2rgb(self.colors["layer3"])

    def algo_woodland_family(self, final, w, h, scale, dist, blob_size, roughness, hex2rgb, t1, t2, t3):
        if self.current_mode.get() == "Puzzle Inspired": roughness = 0.5 
        warp_x = self.get_noise(h, w, scale * 3, seed_add=50) * dist
        base_scale = scale * (blob_size / 2.0)
        n1 = self.get_noise(h, w, base_scale, seed_add=100)
        n2 = self.get_noise(h, w, base_scale, seed_add=200)
        n3 = self.get_noise(h, w, base_scale, seed_add=300)
        turb = self.get_noise(h, w, scale/2, seed_add=400) * (roughness / 10.0)
        n1 += turb; n2 += turb; n3 += turb
        if self.layer_vars['layer1'].get(): final[n1 > t1] = hex2rgb(self.colors["layer1"])
        if self.layer_vars['layer2'].get(): final[n2 > t2] = hex2rgb(self.colors["layer2"])
        if self.layer_vars['layer3'].get(): final[n3 > t3] = hex2rgb(self.colors["layer3"])

    def algo_chocolate(self, final, w, h, scale, dist, blob_size, chip_size, hex2rgb, t1, t2, t3):
        self.algo_woodland_family(final, w, h, scale, dist, blob_size, 20.0, hex2rgb, t1, t2, t3)
        if self.layer_vars['layer2'].get(): 
            chip_scale = scale / 4.0
            chips = self.get_noise(h, w, chip_scale, seed_add=999)
            mask_shadow = chips > t3
            mask_center = chips > (t3 + 0.05)
            final[mask_shadow] = hex2rgb(self.colors["layer2"]) 
            final[mask_center] = hex2rgb(self.colors["layer3"]) 

    def algo_flecktarn(self, final, w, h, scale, dist, density, dot_size, hex2rgb, t1, t2, t3):
        region_scale = scale * 2.5
        reg1 = self.get_noise(h, w, region_scale, seed_add=500)
        reg2 = self.get_noise(h, w, region_scale, seed_add=600)
        reg3 = self.get_noise(h, w, region_scale, seed_add=700)
        mix = self.get_noise(h, w, scale, seed_add=800) * (dist / 100.0)
        reg1 += mix; reg2 += mix; reg3 += mix
        dot_scale = max(2.0, dot_size) 
        dots = self.get_noise(h, w, dot_scale, seed_add=900)
        dot_thresh = 1.0 - (density / 18.0)
        if self.layer_vars['layer1'].get(): final[(reg1 > t1) & (dots > dot_thresh)] = hex2rgb(self.colors["layer1"])
        if self.layer_vars['layer2'].get(): final[(reg2 > t2) & (dots > dot_thresh)] = hex2rgb(self.colors["layer2"])
        if self.layer_vars['layer3'].get(): final[(reg3 > t3) & (dots > dot_thresh)] = hex2rgb(self.colors["layer3"])

    def save_image(self):
        fp = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if fp:
            ImageTk.getimage(self.tk_img).save(fp)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    app = UniversalCamoGen(root)
    root.mainloop()
