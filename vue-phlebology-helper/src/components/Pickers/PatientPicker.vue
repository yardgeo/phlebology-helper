<template>
    <v-select
            v-model="model"
            :items="patients"
            item-value="ID"
            item-text="MainDicomTags.PatientName"
            label="Паиценты"
            hide-details
            :menu-props="{ closeOnClick: true }"
    >
        <template v-slot:selection="{ item }">
            <span>{{ item.MainDicomTags.PatientName }}</span>
        </template>
    </v-select>
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
                set(value) {
                    this.selectPatient(value);
                }
            }
        },
        methods: {
            ...mapActions("Dicom", [
                "fetchPatients",
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
