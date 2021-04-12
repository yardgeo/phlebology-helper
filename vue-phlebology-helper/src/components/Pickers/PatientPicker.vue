<template>
    <v-autocomplete
            v-model="model"
            :items="patients"
            item-value="id"
            item-text="name"
            label="Пациент"
            hide-details
            :menu-props="{ closeOnClick: true }"
    >
        <template v-slot:selection="{ item }">
            <span>{{ item.name }}</span>
        </template>
    </v-autocomplete>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";
    export default {
        name: "PatientPicker",
        computed: {
            ...mapGetters({
                patients: 'Dicom/getPatients',
                patientsId: 'Dicom/getPatientsId',
            }),
            model: {
                get() {
                    return this.patientsId;
                },
                async set(value) {
                    this.selectPatient(value);
                    await this.fetchStudies(value);
                }
            }
        },
        methods: {
            ...mapActions("Dicom", [
                "fetchPatients",
                "fetchStudies",
                "selectPatient"
            ]),
        },
        async created() {
            if (this.patients.length < 1)
                await this.fetchPatients();
        }
    }
</script>

<style scoped>

</style>
