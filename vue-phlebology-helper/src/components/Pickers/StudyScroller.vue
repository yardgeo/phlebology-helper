<template>
    <v-list>
        <template v-for="(item, index) in items">
            <v-divider
                    :key="index"
            ></v-divider>
            <v-list-item :key="item.id" two-line>
                <v-list-item-avatar>
                    <v-avatar
                            :color="randomColor()"
                            size="80"
                            class="white--text"
                    >
                        {{ item.description }}
                    </v-avatar>
                </v-list-item-avatar>

                <v-list-item-content>
                    <v-list-item-title> Исследование №{{index + 1}}</v-list-item-title>
                    <v-list-item-subtitle>от {{item.studyDate | formatDate }}</v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-action>
                    <v-btn
                            depressed
                            small
                            @click="chooseStudy(index)"
                    >
                        Просмотр

                        <v-icon
                                color="orange darken-2"
                                right
                        >
                            mdi-open-in-new
                        </v-icon>
                    </v-btn>
                </v-list-item-action>
            </v-list-item>
        </template>
    </v-list>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    export default {
        name: "StudyScroller",
        data: () => ({
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
            chooseStudy(index) {
                this.selectStudy(index);
                this.$emit('addDicom');
            }
        },
    }

</script>

<style scoped>

</style>
