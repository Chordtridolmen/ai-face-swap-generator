// ai-face-swap-generator — optional C# interop shim.
// Used by the Windows tray companion (see desktop/ in releases).
using System;
using System.Runtime.InteropServices;

namespace AiFaceSwap.Interop
{
    internal static class FaceSwapInterop
    {
        private const string Dll = "ai_faceswap_native.dll";

        [DllImport(Dll, CallingConvention = CallingConvention.Cdecl)]
        private static extern int aifs_init(string modelPath);

        [DllImport(Dll, CallingConvention = CallingConvention.Cdecl)]
        private static extern int aifs_swap_frame(ref byte bgra, int width, int height);

        public static bool Init(string modelPath) => aifs_init(modelPath) == 0;

        public static bool SwapFrame(byte[] bgra, int width, int height)
        {
            if (bgra == null || bgra.Length != width * height * 4)
                throw new ArgumentException("ai-face-swap-generator: bad BGRA buffer");
            return aifs_swap_frame(ref bgra[0], width, height) == 0;
        }
    }
}