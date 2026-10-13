// ai-face-swap-generator — optional C++ pixel-blend kernel.
// Exposed to Python via pybind11 (see build hook in scripts/build_native.py).
#include <cstdint>
#include <vector>

namespace aifs {

// Alpha-blend two BGRA buffers in place. src and dst must be the same
// length (width * height * 4). alpha in [0, 1].
void blend_bgra_inplace(std::vector<std::uint8_t>& dst,
                        const std::vector<std::uint8_t>& src,
                        float alpha) {
    if (dst.size() != src.size()) return;
    const float inv = 1.0f - alpha;
    for (std::size_t i = 0; i < dst.size(); i += 4) {
        for (int c = 0; c < 3; ++c) {
            const float a = static_cast<float>(src[i + c]);
            const float b = static_cast<float>(dst[i + c]);
            dst[i + c] = static_cast<std::uint8_t>(a * alpha + b * inv);
        }
    }
}

}  // namespace aifs