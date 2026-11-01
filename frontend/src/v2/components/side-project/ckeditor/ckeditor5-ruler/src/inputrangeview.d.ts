/**
 * @license Copyright (c) 2003-2024, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
 */
import { View } from "ckeditor5";
/**
 * A view that represents a single range input element. It is based on a native input element with the `type="range"`.
 */
export default class InputRangeView extends View<HTMLInputElement> {
    /**
     * The side of the slider (as in margin *left* or *right*) it refers to.
     */
    readonly side: SliderSide;
    constructor({ className, side, onChange, }: {
        className: string;
        side: SliderSide;
        onChange: SliderChangeCallback;
    });
    /**
     * Sets the value of the range input. The value must be a number between 0 and 100.
     */
    setValue(newValue: number): void;
    /**
     * A static helper that returns the width of the thumb (handle) of the range input. It cannot be obtained in another way
     * as it is a private (shadow DOM) part of the native `<input>` component. Used for calculations.
     */
    static get rulerThumbWidth(): number;
}
export type SliderSide = "left" | "right";
/**
 * A callback called when the user moves the slider. The value is a number between 0 and 100
 * and must be interpolated to the pixel width.
 */
export type SliderChangeCallback = (value: number, side: SliderSide) => void;
