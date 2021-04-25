<template>
    <v-sheet
            class="mx-auto"
            elevation="0"
    >
        <v-slide-group
                v-model="model"
                center-active
                show-arrows
        >
            <v-slide-item
                    v-for="instance in instances"
                    :key="instance.id"
                    v-slot="{ active, toggle }"
            >
                <v-card
                        :color="active ? 'orange darken-2' : 'grey lighten-1'"
                        class="ma-4 ml-0"
                        height="100"
                        width="100"
                        :style="'border: 1px solid red;'"
                        @click="toggle"
                >
                    <v-img :src="instance.preview" lazy-src="../../assets/venousPlaceholder.jpeg">
                        <template v-slot:placeholder>
                            <v-row
                                    class="fill-height ma-0"
                                    align="center"
                                    justify="center"
                            >
                                <v-progress-circular
                                        indeterminate
                                        color="grey lighten-5"
                                ></v-progress-circular>
                            </v-row>
                        </template>
                    </v-img>
                    <v-row
                            class="fill-height"
                            align="center"
                            justify="center"
                    >
                        <v-scale-transition>
                            <v-icon
                                    v-if="active"
                                    color="white"
                                    size="48"
                                    v-text="'mdi-close-circle-outline'"
                            ></v-icon>
                        </v-scale-transition>
                    </v-row>
                </v-card>
            </v-slide-item>
        </v-slide-group>
    </v-sheet>
</template>

<script>
    import {mapGetters} from "vuex";

    export default {
        name: "SeriesScroller",
        data() {
            return {
            }
        },
        computed: {
            ...mapGetters({
                series: 'Dicom/getChosenSeries',
                sliceNumber: "Dicom/getCurrentSliceNumber"
            }),
            model: {
                get() {
                    return this.sliceNumber;
                },
                set(value) {
                    if (!this.series) {
                        return;
                    }
                    this.$emit('changeCurrentSliceNumberFromSlider', value);
                }
            },
            instances() {
                if (!this.series) {
                    return [{id: 0, preview: ''},
                        {id: 1, preview: ''},
                        {id: 2, preview: ''},
                        {id: 3, preview: ''}];
                }
                return this.series.instances;
            },
        },
        methods: {
        }
    }

</script>

<style scoped>

</style>
