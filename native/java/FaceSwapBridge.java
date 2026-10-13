// ai-face-swap-generator — optional Java JNI bridge.
// Backs the batch exporter in desktop-tools/faceswap-batch.jar.
package dev.aifaceswap.bridge;

public final class FaceSwapBridge {
    static { System.loadLibrary("ai_faceswap_native"); }

    private FaceSwapBridge() {}

    private static native int nativeInit(String modelPath);
    private static native int nativeSwapFrame(byte[] bgra, int width, int height);

    public static boolean init(String modelPath) {
        return nativeInit(modelPath) == 0;
    }

    public static boolean swapFrame(byte[] bgra, int width, int height) {
        if (bgra == null || bgra.length != width * height * 4) {
            throw new IllegalArgumentException("ai-face-swap-generator: bad BGRA buffer");
        }
        return nativeSwapFrame(bgra, width, height) == 0;
    }
}