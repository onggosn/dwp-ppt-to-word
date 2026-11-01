/**
 * @license Copyright (c) 2003-2024, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
 */
import { View } from "ckeditor5";
import { type SliderChangeCallback } from "./inputrangeview";
import "../theme/ruler.css";
/**
 * Represents the ruler UI component with three sliders: left and right margins, and the text indent.
 */
export default class RulerView extends View {
    /**
     * When `false` the ruler will not display the handles or allow for changing their values.
     */
    isEnabled: boolean;
    /**
     * @internal
     */
    private readonly _marginLeftSlider;
    /**
     * @internal
     */
    private readonly _marginRightSlider;
    /**
     * @internal
     */
    private readonly _textIndentSlider;
    /**
     *
     * @param onMarginChange The callback called when the user moves the margin sliders.
     * @param onIndentChange The callback called when the user moves the text indent slider.
     */
    constructor(onMarginChange: SliderChangeCallback, onIndentChange: SliderChangeCallback);
    /**
     * Sets the value of the sliders.
     *
     * Each slider value must be in [0,100] range.
     */
    setValue({ marginLeft, marginRight, textIndent, }: {
        marginLeft: number;
        marginRight: number;
        textIndent: number;
    }): void;
}
