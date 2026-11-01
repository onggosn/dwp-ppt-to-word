/**
 * @license Copyright (c) 2003-2024, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
 */
import { Plugin } from "ckeditor5";
import RulerView from "./rulerview";
/**
 * The Ruler plugin. It provides a ruler UI component that allows the user to set the left and right margin and the text indent
 * of certain block in the editor content.
 */
export default class Ruler extends Plugin {
    /**
     * The reference to the ruler view instance. Can be added to the toolbar container or any other place in the UI
     * as long as it retains 100% width of the editing root in DOM.
     */
    rulerView: RulerView;
    /**
     * Used to observe the ruler view element for resize events and update the ruler.
     *
     * @internal
     */
    private _resizeObserver;
    /**
     * @inheritDoc
     */
    static get pluginName(): "Ruler";
    init(): void;
    destroy(): void;
    /**
     * Renders the #rulerView and registers it in the editor UI.
     *
     * **Note**: It's up to the integrator where the ruler should be placed in the UI when the editor is ready.
     *
     * @internal
     */
    private _setupRulerView;
    /**
     * Attaches listeners to the editor's events to update the ruler view. The rules gets updated whenever the
     * editor's view is rendered or the editor is resized.
     *
     * @internal
     */
    private _setupRulerUpdates;
    /**
     * Enables 'marginLeft', 'marginRight', and 'textIndent' model attributes on supported model elements.
     *
     * Those attributes are used to store the left and right margin and the text indent of the block elements.
     *
     * It also enables upcast and downcast conversion for those attributes for the data to be properly loaded into the editor (upcast)
     * and then rendered in the view or obtained using `editor.getData()` (downcast).
     *
     * @internal
     */
    private _setupConversion;
    /**
     * Updates the state of the ruler (left, right margin and the text indent sliders) view according to the current user selection.
     * The first selected supported $block element is used as a source of the state.
     *
     * @internal
     */
    private _updateRuler;
    /**
     * Returns the left and right offset of the view element relative to the bounding rect of the root element.
     *
     * @internal
     */
    private _getElementRootOffset;
    /**
     * Returns the list of block elements that can be used with the ruler. By default, paragraphs and all heading elements are allowed.
     *
     * @internal
     */
    private _getAllowedBlockNames;
    /**
     * Returns all currently selected block elements that allow margin and text indent attributes.
     *
     * @internal
     */
    private _getSelectedAllowedBlocks;
    /**
     * A callback executed when the user changed the margin in the #rulerView. It updates the margin of the selected block elements
     * that support it.
     *
     * @internal
     */
    private _onRulerMarginChange;
    /**
     * * A callback executed when the user changed the text indent in the #rulerView. It updates the text indent of the
     * selected block elements that support it.
     *
     * @internal
     */
    private _onRulerTextIndentChange;
    /**
     * Normalizes the value retrieved from the ruler view when the user moved the slider.
     *
     * @internal
     */
    private _normalizeRulerValue;
}
