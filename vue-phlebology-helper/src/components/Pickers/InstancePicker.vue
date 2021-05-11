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
                    v-for="(instance, index) in instances"
                    :key="instance.id"
                    v-slot="{ active, toggle }"
            >
                <v-card
                        :color="active ? 'orange darken-2' : 'grey lighten-1'"
                        class="ma-4 ml-0"
                        height="100"
                        width="100"
                        :style="'border: 1px solid;'"
                        @click="toggle"
                >
                    <v-img :src="instance.preview" lazy-src="../../assets/venousPlaceholder.jpeg">
                        <v-icon
                                v-if="markedSlices.includes(index.toString())"
                                right
                                small
                                color="orange darken-2"
                        >
                            mdi-marker
                        </v-icon>
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
                </v-card>
            </v-slide-item>
        </v-slide-group>
    </v-sheet>
</template>

<script>
    import {mapGetters} from "vuex";

    export default {
        name: "InstancePicker",
        data() {
            return {
            }
        },
        computed: {
            ...mapGetters({
                series: 'Dicom/getChosenSeries',
                sliceNumber: "Dicom/getCurrentSliceNumber",
                markedSlices: "Dicom/getMarkedSlices"
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
            marked(id) {
                let index = this.series.instances.findIndex(ins => ins.id === id);
                console.log(index, this.markedSlices, index.toString() in this.markedSlices);
                return index.toString() in this.markedSlices;
            },
        }
    }

</script>

<style scoped>

</style>
