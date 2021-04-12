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
                    cols="4"
            >
                <v-card v-if="this.chosenPatient"
                        :loading="this.studies.length === 0"
                >
                    <study-scroller @addDicom="addDicom(0)"></study-scroller>
                </v-card>
            </v-col>
            <v-col
                    cols="8"

            >
                <v-row
                        align="center"
                        justify="center"
                >
                    <v-card min-width="600px" min-height="600px">
                        <v-container fluid>
                            <v-row align="start" justify="center">
                                <v-col>
                                    <div id="dwv">
                                        <div class="layerContainer">
                                            <canvas class="imageLayer" id="canvas1"></canvas>
                                            <div class="drawDiv"></div>
                                        </div>
                                    </div>
                                    <v-card-text class="pt-5">
                                        <v-slider
                                                v-if="loadItem > 0"
                                                label="Срез"
                                                v-model="slice"
                                                :max="loadItem"
                                        >
                                        </v-slider>
                                    </v-card-text>
                                </v-col>
                                <v-col
                                        v-if="this.rotation > -1">
                                    <v-btn-toggle
                                            color="black"
                                            dark
                                            dense
                                            mandatory
                                            v-model="rotation"
                                            background-color="orange darken-2"
                                    >
                                        <v-btn
                                                x-large
                                                icon
                                        >
                                            <v-icon>mdi-axis-x-arrow</v-icon>
                                        </v-btn>
                                        <v-btn
                                                x-large
                                                icon
                                        >
                                            <v-icon>mdi-axis-y-arrow</v-icon>
                                        </v-btn>
                                        <v-btn
                                                x-large
                                                icon
                                        >
                                            <v-icon>mdi-axis-z-arrow</v-icon>
                                        </v-btn>
                                    </v-btn-toggle>
                                    <div class="my-5">
                                        <v-btn
                                                x-large
                                                icon
                                                :color="drawButtonColor"
                                                @click="drawClick"
                                        >
                                            <v-icon>mdi-fountain-pen</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="my-5">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="zoomPlus"
                                        >
                                            <v-icon>mdi-magnify-plus-outline</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="my-5">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="zoomMinus"
                                        >
                                            <v-icon>mdi-magnify-minus-outline</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="my-5">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="reset"
                                        >
                                            <v-icon>mdi-reload</v-icon>
                                        </v-btn>
                                    </div>
                                    <div class="my-5">
                                        <v-btn
                                                x-large
                                                icon
                                                @click="download"
                                        >
                                            <v-icon>mdi-download</v-icon>
                                        </v-btn>
                                    </div>
                                </v-col>
                            </v-row>
                            <v-row></v-row>
                        </v-container>
                    </v-card>
                </v-row>
                <v-row>
                </v-row>

            </v-col>
            <canvas id="test" height="1000px" width="1000px"></canvas>

        </v-row>
    </v-container>
</template>

<script>
    import PatientPicker from "../components/Pickers/PatientPicker"
    import StudyScroller from "../components/Pickers/StudyScroller"
    import dwv from 'dwv';
    var fs=require('fs');

    dwv.gui.getElement = dwv.gui.base.getElement;


    import AuthService from '@/services/auth.service';
    import {mapActions, mapGetters} from "vuex";

    export default {
        name: "Dashboard",
        components: {StudyScroller, PatientPicker},
        data() {
            return {
                dwvApp: null,
                test: 0,
                loadItem: 0,
                drawStatus: false,
                drawButtonColor: "white",
                currentRotate: -1,
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
                studies: 'Dicom/getStudies'
            }),
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
                "fetchStudies"
            ]),
            download() {
                let filename = "test.png";
                let canvas = document.getElementById("test");
                let canvas1 = document.getElementById("canvas1");
                let canvas2 = document.getElementsByClassName("konvajs-content")[0].children[0];

                var context = canvas.getContext('2d');
                canvas1.width = 1000; // in pixels
                canvas1.height = 1000; // in pixels
                context.drawImage(canvas1, 0, 0);
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
            },
            loadJSON(callback) {
                var xobj = new XMLHttpRequest();
                xobj.overrideMimeType("application/json");
                xobj.open('GET', 'my_data.json', true);
                // Replace 'my_data' with the path to your file
                xobj.onreadystatechange = function () {
                    if (xobj.readyState === 4 && xobj.status === 200) {
                        // Required use of an anonymous callback
                        // as .open() will NOT return a value but simply returns undefined in asynchronous mode
                        callback(xobj.responseText);
                    }
                }
                    xobj.send(null);
            },
            reset() {
                console.log(this.dwvApp.getState());
                console.log("sdfd");
                var data=fs.readFileSync('../assets/test.json', 'utf8');
                this.dwvApp.loadFiles([data]);

                this.dwvApp.resetDisplay();
            },
            zoomPlus() {
                this.dwvApp.setTool("ZoomAndPan");
                this.dwvApp.stepZoom(0.1, 250, 250);
            },
            zoomMinus() {
                this.dwvApp.setTool("ZoomAndPan");
                this.dwvApp.stepZoom(-0.1, 250, 250);

            },
            drawClick() {
                this.drawStatus = !this.drawStatus;
                if (this.drawStatus === true) {
                    this.drawOn();
                } else {
                    this.drawOff();
                }
            },
            drawOn() {
                this.drawButtonColor = 'orange darken-2';
                this.dwvApp.setTool("Draw");
                this.dwvApp.setDrawShape(this.tools.Draw.options[0]);
            },
            drawOff() {
                this.drawButtonColor = 'white';
                this.dwvApp.setTool("Scroll");
            },
            addDicom(i) {

                let urls = [];

                this.chosenStudy.series[i].instances.forEach((ins) => {
                    urls.push(process.env.VUE_APP_API_BASE_URL + 'dicom/' + ins)
                });

                this.currentRotate = i;

                this.dwvApp.loadURLs(urls,
                    [{name: "Authorization", value: 'Bearer ' + AuthService.checkAccessToken()}],
                    true);
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
            this.dwvApp.addEventListener('load-end', (/*event*/) => {
                console.log(this.loadItem, nReceivedError, nReceivedAbort);
                let pos = this.dwvApp.getViewController().getCurrentPosition();
                pos.k = 0;
                this.test = 0;
                this.dwvApp.getViewController().setCurrentPosition(pos);
                --this.loadItem;
            });

            this.dwvApp.addEventListener('load-start', (/*event*/) => {
                this.loadItem = 0;
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

            // handle key events
            this.dwvApp.addEventListener('keydown', event => {
                var pos = "";
                if (event.code === "ArrowRight" && this.dwvApp.getViewController().getCurrentPosition().k < this.loadItem) {
                    this.drawOff();
                    pos = this.dwvApp.getViewController().getCurrentPosition();
                    ++pos.k;
                    this.test++;
                    this.dwvApp.getViewController().setCurrentPosition(pos);
                } else if (event.code === "ArrowLeft" && this.dwvApp.getViewController().getCurrentPosition().k > 0) {
                    this.drawOff();
                    pos = this.dwvApp.getViewController().getCurrentPosition();
                    --pos.k;
                    this.test--;
                    this.slice = pos.k;
                    this.dwvApp.getViewController().setCurrentPosition(pos);
                }
                this.dwvApp.defaultOnKeydown(event);
            });

            // possible load from location
            dwv.utils.loadFromUri(window.location.href, this.dwvApp);
            // handle window resize
            window.addEventListener('resize', this.dwvApp.onResize)
// load dicom data

        }
    }
</script>

<style scoped>
    #dwv {
        font-family: Arial, Helvetica, sans-serif;
        height: 90%;
    }

    ::-webkit-scrollbar {
        width: 0;
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: transparent;
    }

    .layerContainer {
        min-width: 500px;
        min-height: 500px;
    }

    /* Layers */
    .v-btn-toggle {
        flex-direction: column;
    }
</style>
