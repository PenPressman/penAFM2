import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm


def plot_height_map(arr, pixel_scale_nm, output_path):
    """Save a publication-quality AFM height map as a 300 dpi TIFF.

    Parameters
    ----------
    arr : ndarray, shape (M, N)
        Flattened height data in metres.
    pixel_scale_nm : float
        Physical size of one pixel in nanometres.
    output_path : str or Path
        Destination path; should end in .tiff or .tif.
    """
    arr_nm = arr * 1e9  # convert metres → nm for display

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(arr_nm, cmap="afmhot", origin="upper")
    ax.axis("off")

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.08)
    cbar = fig.colorbar(im, cax=cax)
    cbar.set_label("Height (nm)", fontsize=10)
    cbar.ax.tick_params(labelsize=8)

    # Scale bar: pick a round length that is ~15% of image width
    image_width_nm = arr_nm.shape[1] * pixel_scale_nm
    raw = image_width_nm * 0.15
    magnitude = 10 ** np.floor(np.log10(raw))
    scale_nm = round(raw / magnitude) * magnitude
    scale_px = scale_nm / pixel_scale_nm

    label = f"{int(scale_nm)} nm" if scale_nm < 1000 else f"{scale_nm/1000:.3g} µm"
    scalebar = AnchoredSizeBar(
        ax.transData,
        scale_px,
        label,
        loc="lower right",
        pad=0.5,
        color="white",
        frameon=False,
        size_vertical=scale_px * 0.04,
        fontproperties=fm.FontProperties(size=10, weight="bold"),
        label_top=False,
    )
    ax.add_artist(scalebar)

    fig.savefig(output_path, dpi=300, format="tiff",
                bbox_inches="tight", pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)
