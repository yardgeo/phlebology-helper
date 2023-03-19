<template>
    <v-list>
        <v-list-item-group
                v-model="selectedWrapper"
                active-class="chosen"
        >
        <template v-for="(series, index) in study.series">
            <v-divider
                    :key="index"
            ></v-divider>
            <v-list-item :key="series.id" three-line>

                <v-list-item-content>
                    <v-list-item-title> Серия №{{index + 1}}</v-list-item-title>
                    Угол исследования {{series.orientation}}
                </v-list-item-content>
            </v-list-item>
        </template>
        </v-list-item-group>
    </v-list>
</template>

<script>
    import {mapGetters} from "vuex";

    export default {
        name: "SeriesScroller",
        data() {
            return {
                selected: null,
            }
        },
        computed: {
            ...mapGetters({
                study: 'Dicom/getChosenStudy',
            }),
            selectedWrapper: {
                get() {
                    return this.selected;
                },
                async set(value) {
                    await this.chooseSeries(value);
                }
            },
        },
        methods: {
            genRandomIndex(length) {
                return Math.ceil(Math.random() * (length - 1))
            },
            randomColor() {
                return this.colors[this.genRandomIndex(this.colors.length)];
            },
            async chooseSeries(index) {
                this.$emit('addDicom', index);
                this.selected = index;
            }
        }
    }

</script>

<style scoped>
    .chosen {
        border: 1px solid #F57C00;
    }
</style>
