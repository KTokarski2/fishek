package com.fishek.util;

import com.fishek.gui.AddWordWindow;
import com.github.kwhat.jnativehook.GlobalScreen;
import com.github.kwhat.jnativehook.NativeHookException;
import com.github.kwhat.jnativehook.keyboard.NativeKeyEvent;
import com.github.kwhat.jnativehook.keyboard.NativeKeyListener;

public class GlobalHotkey implements NativeKeyListener {

    private boolean ctrl;
    private boolean shift;

    public static void register() {
        try {
            GlobalScreen.registerNativeHook();
            GlobalScreen.addNativeKeyListener(new GlobalHotkey());
            java.util.logging.Logger logger = java.util.logging.Logger.getLogger(GlobalScreen.class.getPackage().getName());
            logger.setLevel(java.util.logging.Level.OFF);

        } catch (NativeHookException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void nativeKeyPressed(NativeKeyEvent e) {
        System.out.println("Key pressed: " + e.getKeyText(e.getKeyCode()));
        if (e.getKeyCode() == NativeKeyEvent.VC_CONTROL) ctrl = true;
        if (e.getKeyCode() == NativeKeyEvent.VC_SHIFT) shift = true;
        if (e.getKeyCode() == NativeKeyEvent.VC_F9 && ctrl && shift) {
            String text = ClipboardUtil.getText();
            if (!text.isBlank()) {
                AddWordWindow.show(text);
            }
        }
    }

    @Override
    public void nativeKeyReleased(NativeKeyEvent e) {
        if (e.getKeyCode() == NativeKeyEvent.VC_CONTROL) ctrl = false;
        if (e.getKeyCode() == NativeKeyEvent.VC_SHIFT) shift = false;
    }

    @Override
    public void nativeKeyTyped(NativeKeyEvent e) {}
}