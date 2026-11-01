import { InlineEditor, AccessibilityHelp, Alignment, Autoformat, AutoLink, Autosave, BlockQuote, Bold, CKBox, CKBoxImageEdit, CloudServices, Code, Essentials, FindAndReplace, FontBackgroundColor, FontColor, FontFamily, FontSize, GeneralHtmlSupport, Heading, Highlight, HorizontalLine, Image, ImageBlock, ImageCaption, ImageInline, ImageInsert, ImageInsertViaUrl, ImageResize, ImageStyle, ImageTextAlternative, ImageToolbar, ImageUpload, Indent, IndentBlock, Italic, Link, LinkImage, List, ListProperties, MediaEmbed, Mention, PageBreak, Paragraph, PasteFromOffice, PictureEditing, RemoveFormat, SelectAll, ShowBlocks, SpecialCharacters, SpecialCharactersArrows, SpecialCharactersCurrency, SpecialCharactersEssentials, SpecialCharactersLatin, SpecialCharactersMathematical, SpecialCharactersText, Strikethrough, Style, Subscript, Superscript, Table, TableCaption, TableCellProperties, TableColumnResize, TableProperties, TableToolbar, TextPartLanguage, TextTransformation, TodoList, Underline, Undo, WordCount, PlainTableOutput } from "ckeditor5";
import { CaseChange, Comments, ExportPdf, ExportWord, FormatPainter, ImportWord, PasteFromOfficeEnhanced, PresenceList, RealTimeCollaborativeComments, RealTimeCollaborativeEditing, RealTimeCollaborativeRevisionHistory, RealTimeCollaborativeTrackChanges, RevisionHistory, SlashCommand, TableOfContents, Template, TrackChanges, TrackChangesData } from "ckeditor5-premium-features";
import "ckeditor5/ckeditor5.css";
import "ckeditor5-premium-features/ckeditor5-premium-features.css";
import "./style.css";
import "./fonts.css";
import Ruler from "../ckeditor5-ruler/src/ruler";
declare class CustomInline extends InlineEditor {
    static builtinPlugins: (typeof AccessibilityHelp | typeof Alignment | typeof Autoformat | typeof AutoLink | typeof Autosave | typeof BlockQuote | typeof Bold | typeof CaseChange | typeof CKBox | typeof CKBoxImageEdit | typeof CloudServices | typeof Code | typeof Comments | typeof Essentials | typeof ExportPdf | typeof ExportWord | typeof FindAndReplace | typeof FontBackgroundColor | typeof FontColor | typeof FontFamily | typeof FontSize | typeof FormatPainter | typeof GeneralHtmlSupport | typeof Heading | typeof Highlight | typeof HorizontalLine | typeof ImageBlock | typeof ImageCaption | typeof ImageInline | typeof ImageInsert | typeof ImageInsertViaUrl | typeof ImageResize | typeof ImageStyle | typeof ImageTextAlternative | typeof ImageToolbar | typeof ImageUpload | typeof ImportWord | typeof Indent | typeof IndentBlock | typeof Italic | typeof Link | typeof LinkImage | typeof List | typeof ListProperties | typeof MediaEmbed | typeof Image | typeof Mention | typeof PageBreak | typeof Paragraph | typeof PasteFromOffice | typeof PasteFromOfficeEnhanced | typeof PictureEditing | typeof PresenceList | typeof RealTimeCollaborativeComments | typeof RealTimeCollaborativeEditing | typeof RealTimeCollaborativeRevisionHistory | typeof RealTimeCollaborativeTrackChanges | typeof RemoveFormat | typeof RevisionHistory | typeof SelectAll | typeof ShowBlocks | typeof SlashCommand | typeof SpecialCharacters | typeof SpecialCharactersArrows | typeof SpecialCharactersCurrency | typeof SpecialCharactersEssentials | typeof SpecialCharactersLatin | typeof SpecialCharactersMathematical | typeof SpecialCharactersText | typeof Strikethrough | typeof Style | typeof Subscript | typeof Superscript | typeof Table | typeof TableCaption | typeof TableCellProperties | typeof TableColumnResize | typeof TableOfContents | typeof TableProperties | typeof TableToolbar | typeof PlainTableOutput | typeof Template | typeof TextPartLanguage | typeof TextTransformation | typeof TodoList | typeof TrackChanges | typeof TrackChangesData | typeof Underline | typeof Undo | typeof WordCount | typeof Ruler)[];
    static defaultConfig: {
        toolbar: {
            items: (string | {
                label: string;
                icon: string;
                items: string[];
            })[];
            shouldNotGroupWhenFull: boolean;
        };
        list: {
            properties: {
                styles: boolean;
                startIndex: boolean;
                reversed: boolean;
            };
        };
        sidebar: {
            preventScrollOutOfView: boolean;
        };
        link: {
            addTargetToExternalLinks: boolean;
            defaultProtocol: string;
            decorators: {
                toggleDownloadable: {
                    mode: string;
                    label: string;
                    attributes: {
                        download: string;
                    };
                };
            };
        };
        alignment: {
            options: string[];
        };
        image: {
            styles: string[];
            resizeOptions: {
                name: string;
                label: string;
                value: string;
            }[];
            toolbar: string[];
            insert: {
                integrations: string[];
            };
        };
        htmlSupport: {
            allow: ({
                name: string;
                classes: string[];
                styles: boolean;
                attributes?: undefined;
            } | {
                name: string;
                classes: string[];
                styles?: undefined;
                attributes?: undefined;
            } | {
                name: RegExp;
                styles: boolean;
                classes?: undefined;
                attributes?: undefined;
            } | {
                name: string;
                styles: boolean;
                attributes: {
                    start: boolean;
                };
                classes?: undefined;
            })[];
            disallow: any[];
        };
        table: {
            contentToolbar: string[];
        };
        pagination: {
            pageWidth: string;
            pageHeight: string;
            pageMargins: {
                top: string;
                bottom: string;
                left: string;
                right: string;
            };
        };
        comments: {
            editorConfig: {
                extraPlugins: (typeof Autoformat | typeof Bold | typeof Italic | typeof List | typeof Mention)[];
                mention: {
                    feeds: {
                        marker: string;
                        feed: any[];
                    }[];
                };
            };
        };
        mediaEmbed: {
            toolbar: string[];
        };
        caseChange: {
            titleCase: {
                excludeWords: string[];
            };
        };
        style: {
            definitions: {
                name: string;
                element: string;
                classes: string[];
            }[];
        };
        heading: {
            options: ({
                model: string;
                title: string;
                class: string;
                view?: undefined;
            } | {
                model: string;
                view: string;
                title: string;
                class: string;
            })[];
        };
        fontFamily: {
            supportAllValues: boolean;
            options: string[];
        };
        fontSize: {
            options: {
                title: string;
                model: string;
            }[];
            supportAllValues: boolean;
        };
        htmlEmbed: {
            showPreviews: boolean;
        };
    };
}
export default CustomInline;
