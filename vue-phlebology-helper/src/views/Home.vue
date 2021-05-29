<template>
    <v-container fluid full-height>
        <v-toolbar>

            <!--      <v-toolbar-title>Просмоторщик</v-toolbar-title>-->
            <v-row>
                <v-col
                        cols="4">
                    <PatientPicker></PatientPicker>
                </v-col>
            </v-row>
        </v-toolbar>
        <v-row>
            <v-col
                    cols="3"
            >
                <v-card v-if="this.chosenPatient"
                        :loading="this.studies.length === 0"
                >
                    <study-scroller></study-scroller>
                </v-card>
            </v-col>
            <v-col
                    cols="6"
            >
                    <v-card :loading="!this.loadFinish" flex-grow-1>
                        <v-container fluid>
                            <v-row align="start" justify="center" no-gutters>
                                <v-col cols="11">
                                    <div id="dwv">
                                    <div class="layerContainer">
                                            <canvas class="imageLayer" id="canvas1"></canvas>
                                            <div class="drawDiv"></div>
                                        </div>
                                    </div>
                                    <InstancePicker  @changeCurrentSliceNumberFromSlider="changeCurrentSliceNumberFromSlider"/>
                                </v-col>
                                <v-col
                                        cols="1"
                                        v-if="this.rotation > -1">
                                    <div class="mt-4">
                                        <v-btn
                                                x-large
                                                icon
                                                :color="drawButtonColor"
                                                @click="drawClick"
                                        >
                                            <v-icon>mdi-fountain-pen</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="mt-4">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="undo"
                                        >
                                            <v-icon>mdi-undo</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="mt-4">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="redo"
                                        >
                                            <v-icon>mdi-redo</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="mt-4">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="zoomPlus"
                                        >
                                            <v-icon>mdi-magnify-plus-outline</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="mt-4">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="zoomMinus"
                                        >
                                            <v-icon>mdi-magnify-minus-outline</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="mt-4">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="saveState"
                                        >
                                            <v-icon>mdi-content-save</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="mt-4">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="download"
                                        >
                                            <v-icon>mdi-download</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="mt-4">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="pastPrev"
                                        >
                                            <v-icon>mdi-content-paste</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="mt-4">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="autoSegment"
                                        >
                                            <v-icon>mdi-brightness-auto</v-icon>
                                        </v-btn>
                                    </div>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card>
            </v-col>
            <v-col cols="3" >
                <v-card v-if="studyIsChosen"
                >
                    <SeriesPicker @addDicom="addDicom"/>
                </v-card>
            </v-col>
            <canvas id="downloadCanvas" width="564px" height="564px"></canvas>
        </v-row>
    </v-container>
</template>

<script>
    import PatientPicker from "../components/Pickers/PatientPicker"
    import StudyScroller from "../components/Pickers/StudyScroller"
    import InstancePicker from "../components/Pickers/InstancePicker";
    import SeriesPicker from "../components/Pickers/SeriesPicker";
    import dwv from 'dwv';

    dwv.gui.getElement = dwv.gui.base.getElement;
    // prompt
    // (no direct assign to avoid Illegal invocation error
    // see: https://stackoverflow.com/questions/9677985/uncaught-typeerror-illegal-invocation-in-chrome)
    dwv.gui.prompt = function (message, def) {
        return prompt(message, def)
    };

    // Image decoders (for web workers)
    dwv.image.decoderScripts = {
        jpeg2000: 'assets/dwv/decoders/pdfjs/decode-jpeg2000.js',
        'jpeg-lossless': 'assets/dwv/decoders/rii-mango/decode-jpegloss.js',
        'jpeg-baseline': 'assets/dwv/decoders/pdfjs/decode-jpegbaseline.js',
        rle: 'assets/dwv/decoders/dwv/decode-rle.js'
    };


    import AuthService from '@/services/auth.service';
    import {mapActions, mapGetters} from "vuex";

    export default {
        name: "Dashboard",
        components: {StudyScroller, PatientPicker, InstancePicker, SeriesPicker},
        data() {
            return {
                model:null,
                dwvApp: null,
                test: 0,
                loadItem: 0,
                loadFinish: true,
                drawStatus: false,
                drawButtonColor: "white",
                currentRotate: -1,
                currentSeries: null,
                tools: {
                    Scroll: {},
                    ZoomAndPan: {},
                    WindowLevel: {},
                    Draw: {
                        options: ['FreeHand'],
                        type: 'factory',
                        events: ['draw-create', 'draw-change', 'draw-move', 'draw-delete']
                    }
                },
                // empty image
                src: "",
                files: [],
            }
        },
        computed: {
            ...mapGetters({
                chosenPatient: 'Dicom/getChosenPatient',
                chosenStudy: 'Dicom/getChosenStudy',
                studies: 'Dicom/getStudies',
                chosenSeries: "Dicom/getChosenSeries",
                sliceNumber: "Dicom/getCurrentSliceNumber",
                segmentationData: "Dicom/getSegmentData",
            }),
            studyIsChosen() {
                if (!Object.keys(this.chosenStudy).length) {
                    return false;
                }
                return true;
            },
            rotation: {
                get() {
                    return this.currentRotate;
                },
                set(value) {
                    this.currentRotate = value;
                    this.addDicom(value);
                }
            },
            slice: {
                get() {
                    return this.test;
                },
                set(value) {
                    if (this.dwvApp === null || this.dwvApp.getViewController() === null) {
                        return;
                    } else {
                        this.drawOff();
                        var pos = this.dwvApp.getViewController().getCurrentPosition();
                        pos.k = value;
                        this.test = value;
                        this.dwvApp.getViewController().setCurrentPosition(pos);
                    }
                }
            }
        },
        methods: {
            ...mapActions("Dicom", [
                "fetchStudies",
                "uploadState",
                "selectSeries",
                "fetchSegment",
                "changeCurrentSliceNumber",
                "markSlice"
            ]),
            download() {
                let current_position = this.dwvApp.getViewController().getCurrentPosition();
                let current_frame = this.dwvApp.getViewController().getCurrentFrame();

                const filename = `slice-${current_position.k}_frame-${current_frame}.png`;


                let canvas = document.getElementById("downloadCanvas");
                let canvas1 = document.getElementById("canvas1");
                let canvas2 = document.getElementsByClassName("konvajs-content")[0].children[0];

                var context = canvas.getContext('2d');
                context.save();


                context.drawImage(canvas1, 0, 0);
                context.scale(0.5, 0.5);
                context.drawImage(canvas2, 0, 0);
                /// create an "off-screen" anchor tag
                var lnk = document.createElement('a'), e;


                /// the key here is to set the download attribute of the a tag
                lnk.download = filename;


                /// convert canvas content to data-uri for link. When download
                /// attribute is set the content pointed to by link will be
                /// pushed as "download" in HTML5 capable browsers
                lnk.href = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");

                /// create a "fake" click-event to trigger the download
                if (document.createEvent) {
                    e = document.createEvent("MouseEvents");
                    e.initMouseEvent("click", true, true, window,
                        0, 0, 0, 0, 0, false, false, false,
                        false, 0, null);

                    lnk.dispatchEvent(e);
                } else if (lnk.fireEvent) {
                    lnk.fireEvent("onclick");
                }
                context.clearRect(0, 0, canvas.width, canvas.height);

                // Restore the transform
                context.restore();
            },
            pastPrev() {
                this.drawOff();

                let state = JSON.parse(this.dwvApp.getState());
                let current_position = this.dwvApp.getViewController().getCurrentPosition();
                let current_frame = this.dwvApp.getViewController().getCurrentFrame();

                const current_id = `slice-${current_position.k}_frame-${current_frame}`;
                const pred_id = `slice-${current_position.k - 1}_frame-${current_frame}`;

                // find previous drawing
                const i = state.drawings.children.findIndex(draw => draw.attrs.id === pred_id);
                if (i === -1) {
                    return ;
                }

                // create new drawing
                let new_draw = state.drawings;
                new_draw.children = [state.drawings.children[i]];
                new_draw.children[0].attrs.id = current_id;

                this.dwvApp.setDrawings(new_draw, null);
            },
            async autoSegment() {
                this.drawOff();
                this.loadFinish=false;

                let state = JSON.parse(this.dwvApp.getState());
                let current_position = this.dwvApp.getViewController().getCurrentPosition();
                let current_frame = this.dwvApp.getViewController().getCurrentFrame();
                const current_id = `slice-${current_position.k}_frame-${current_frame}`;
                let drawingDetailName = `auto_segmetate_${current_id}`;

                const i = Object.keys(state.drawingsDetails).findIndex(key => key === drawingDetailName);

                if (i !== -1) {
                    this.loadFinish=true;
                    return ;
                }


                await this.fetchSegment(this.chosenSeries.instances[this.sliceNumber].id);


                if (this.segmentationData.length === 0) {
                    await this.$store.dispatch('Snackbar/set', 'Искусственый интелект не нашел венозные каналы на этом снимке');
                    this.loadFinish=true;
                    return ;
                }

                let template = JSON.parse("{\n" +
                    "    \"attrs\": {\n" +
                    "      \"listening\": true,\n" +
                    "      \"visible\": true\n" +
                    "    },\n" +
                    "    \"className\": \"Layer\",\n" +
                    "    \"children\": [\n" +
                    "      {\n" +
                    "        \"attrs\": {\n" +
                    "          \"name\": \"position-group\",\n" +
                    "          \"id\": \"slice-0_frame-0\",\n" +
                    "          \"visible\": true\n" +
                    "        },\n" +
                    "        \"className\": \"Group\",\n" +
                    "        \"children\": [\n" +
                    "        ]\n" +
                    "      }\n" +
                    "    ]\n" +
                    "  }");


                template.children[0].attrs.id  = current_id;
                for (let i = 0; i < this.segmentationData.length; i++) {
                    template.children[0].children.push({
                        attrs: {
                            name: "freeHand-group",
                            visible: true,
                            id: drawingDetailName,
                            draggable: true
                        },
                        className: "Group",
                        children: [
                            {
                                attrs: {
                                    points: this.segmentationData[i],
                                    stroke: "#0400ff",
                                    strokeWidth: 2.048,
                                    name: "shape",
                                    tension: 0.5
                                },
                                className: "Line"
                            },
                            {
                                attrs: {
                                    x: 377,
                                    y: 286,
                                    name: "label"
                                },
                                className: "Label",
                                children: [
                                    {
                                        attrs: {
                                            "fontSize": 12.288,
                                            "fontFamily": "Verdana",
                                            "fill": "#0400ff",
                                            "name": "text"
                                        },
                                        className: "Text"
                                    },
                                    {
                                        "attrs": {
                                            "height": 12.288
                                        },
                                        "className": "Tag"
                                    }
                                ]
                            }
                        ]
                    })
                }

                let template_details = {};
                template_details[drawingDetailName] = {
                    textExpr: "",
                    longText: "",
                    quant: null
                };
                this.dwvApp.setDrawings(template, template_details);

                this.drawOn();
                this.loadFinish=true;
            },
            async saveState() {
                this.drawOff();
                let uploadStateResponse = false;
                await this.uploadState({
                    series_id: this.currentSeries.id,
                    state: JSON.parse(this.dwvApp.getState())
                }).then((response) => uploadStateResponse = response);
                if (uploadStateResponse) {
                    await this.$store.dispatch('Snackbar/set', 'Маска успешно сохранена');
                } else {
                    await this.$store.dispatch('Snackbar/set', 'Произолша ошибка!');
                }
            },
            zoomPlus() {
                this.drawOff();
                this.dwvApp.setTool("ZoomAndPan");
                this.dwvApp.stepZoom(0.1, 250, 250);
            },
            zoomMinus() {
                this.drawOff();
                this.dwvApp.setTool("ZoomAndPan");
                this.dwvApp.stepZoom(-0.1, 250, 250);

            },
            undo() {
                this.dwvApp.undo();
            },
            redo() {
                this.dwvApp.redo();
            },
            drawClick() {
                if (!this.drawStatus) {
                    this.drawOn();
                } else {
                    this.drawOff();
                }
            },
            drawOn() {
                this.drawStatus = true;
                this.drawButtonColor = 'orange darken-2';
                this.dwvApp.setTool("Draw");
                this.dwvApp.setDrawShape(this.tools.Draw.options[0]);
                this.dwvApp.setDrawLineColour("#0400ff");
            },
            drawOff() {
                this.drawStatus = false;
                this.drawButtonColor = 'white';
                this.dwvApp.setTool("Scroll");
            },
            async addDicom(i) {

                // if (this.currentRotate === i) {
                //     return;
                // }

                this.drawOff();

                let urls = [];

                await this.selectSeries(i);

                this.chosenStudy.series[i].instances.forEach((ins) => {
                    urls.push(process.env.VUE_APP_API_BASE_URL + 'dicom/' + ins.id)
                });

                this.currentRotate = i;
                this.currentSeries = this.chosenStudy.series[i];

                this.dwvApp.loadURLs(urls,
                    [{name: "Authorization", value: 'Bearer ' + AuthService.checkAccessToken()}],
                    true);
            },
            changeCurrentSliceNumberFromSlider(i) {
                if (this.dwvApp === null || this.dwvApp.getViewController() === null) {
                    return;
                }
                this.drawOff();
                let pos = this.dwvApp.getViewController().getCurrentPosition();
                pos.k = i;
                this.changeCurrentSliceNumber(pos.k);
                this.dwvApp.getViewController().setCurrentPosition(pos);
            }
        },
        mounted() {
            this.dwvApp = new dwv.App();
            // initialise app
            this.dwvApp.init({
                containerDivId: 'dwv',
                tools: this.tools
            });


            this.dwvApp.setTool("Scroll");
            let nReceivedError = null;
            let nReceivedAbort = null;
            this.dwvApp.addEventListener('load-end', (event) => {
                console.log(this.loadItem, nReceivedError, nReceivedAbort);
                let pos = this.dwvApp.getViewController().getCurrentPosition();
                pos.k = 0;
                this.dwvApp.getViewController().setCurrentPosition(pos);
                if (event.loadtype !== "image") {
                    this.loadFinish=true;
                    return;
                }
                this.changeCurrentSliceNumber(0);
                --this.loadItem;
                if (this.currentSeries.hasState) {
                    let urls = [process.env.VUE_APP_API_BASE_URL + 'series/' + this.chosenSeries.id + "/state.json"];
                    this.dwvApp.loadURLs(urls,
                        [{name: "Authorization", value: 'Bearer ' + AuthService.checkAccessToken()},
                            {name: "Content-Type", value: 'application/json'}],
                        true);
                }
                this.loadFinish=true;
                console.log(this.dwvApp.getLayerContainerSize());
            });

            this.dwvApp.addEventListener('load-start', (event) => {
                if (event.loadtype === "image") {
                    this.loadItem = 0;
                    this.loadFinish=false;
                }
                nReceivedError = 0;
                nReceivedAbort = 0;
            });

            this.dwvApp.addEventListener('load-item', (/*event*/) => {
                ++this.loadItem;
            });
            this.dwvApp.addEventListener('error', (/*event*/) => {
                console.error(event)
                ++nReceivedError;
            });
            this.dwvApp.addEventListener('abort', (/*event*/) => {
                ++nReceivedAbort
            });
            this.dwvApp.addEventListener('draw-create', (/*event*/) => {
                this.markSlice(this.dwvApp.getDrawController().getDrawDisplayDetails());
            });

            this.dwvApp.addEventListener('draw-delete', (/*event*/) => {
                this.markSlice(this.dwvApp.getDrawController().getDrawDisplayDetails());
            });

            // handle key events
            this.dwvApp.addEventListener('keydown', event => {
                var pos = "";
                if (event.code === "ArrowRight" && this.dwvApp.getViewController().getCurrentPosition().k < this.loadItem) {
                    this.drawOff();
                    pos = this.dwvApp.getViewController().getCurrentPosition();
                    ++pos.k;
                    this.test++;
                    this.changeCurrentSliceNumber(pos.k);
                    this.dwvApp.getViewController().setCurrentPosition(pos);
                } else if (event.code === "ArrowLeft" && this.dwvApp.getViewController().getCurrentPosition().k > 0) {
                    this.drawOff();
                    pos = this.dwvApp.getViewController().getCurrentPosition();
                    --pos.k;
                    this.changeCurrentSliceNumber(pos.k);
                    this.slice = pos.k;
                    this.dwvApp.getViewController().setCurrentPosition(pos);
                }
                this.dwvApp.defaultOnKeydown(event);
            });

            // handle window resize
            window.addEventListener('resize', this.dwvApp.onResize);
// load dicom data
//             this.simpleLoad();

        }
    }
</script>

<style scoped>
    #dwv {
        font-family: Arial, Helvetica, sans-serif;
        height: 564px;
    }

    .imageLayer {
        position: absolute;
        left: 0px;
    }

    .drawDiv {
        position: absolute;
        pointer-events: none;
    }

    .layerContainer {
        position: relative;
        padding: 0;
        margin: auto;
        text-align: center;
    }

    #downloadCanvas {
        width: 0px;
        height: 0px;
    }

    /* Layers */
    .v-btn-toggle {
        flex-direction: column;
    }
</style>
