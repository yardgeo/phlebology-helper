<template>
    <v-list>
        <v-list-item-group
                v-model="selectedWrapper"
                active-class="chosen"
        >
        <template v-for="(item, index) in items">
            <v-divider
                    :key="index"
            ></v-divider>
            <v-list-item :key="item.id" two-line>
                <v-row>
                    <v-col cols="2">
                        <v-list-item-avatar>
                            <v-avatar
                                    :color="randomColor()"
                                    class="white--text"
                            >
                                {{ item.description }}
                            </v-avatar>
                        </v-list-item-avatar>
                    </v-col>
                    <v-col cols="10" class="mt-2">
                        <v-list-item-content>
                            <v-list-item-title> Исследование №{{index + 1}}</v-list-item-title>
                            <v-list-item-subtitle>от {{item.studyDate | formatDate }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-col>
                </v-row>
            </v-list-item>
        </template>
        </v-list-item-group>
    </v-list>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";

    export default {
        name: "StudyScroller",
        data: () => ({
                selected: null,
            colors: ['#2196F3', '#90CAF9', '#64B5F6', '#42A5F5', '#1E88E5', '#1976D2', '#1565C0', '#0D47A1', '#82B1FF', '#448AFF', '#2979FF', '#2962FF'],
        }),
        computed: {
            ...mapGetters({
                studies: 'Dicom/getStudies',
            }),
            items: {
                get() {
                    return this.studies;
                }
            },
            selectedWrapper: {
                get() {
                    return this.selected;
                },
                async set(value) {
                    await this.chooseStudy(value);
                }
            }
        },
        methods: {
            ...mapActions("Dicom", [
                "selectStudy",
            ]),
            genRandomIndex(length) {
                return Math.ceil(Math.random() * (length - 1))
            },
            randomColor() {
                return this.colors[this.genRandomIndex(this.colors.length)];
            },
            async chooseStudy(index) {
                await this.selectStudy(index);
                this.selected = index;
            }
        },
    }

</script>

<style scoped>
    .chosen {
        border: 1px solid #F57C00;
    }
</style>
