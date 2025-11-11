<template>
    <div class="flex flex-col min-h-0 text-base">
        <div class="flex items-center justify-between mb-5">
            <div class="flex flex-col space-y-2">
                <div class="text-xl font-semibold text-ink-gray-9">
                    {{ label }}
                </div>
                <div class="text-ink-gray-6 leading-5">
                    {{ __(description) }}
                </div>
            </div>
            <div class="flex items-center space-x-5">
                <Button @click="openForm('new')">
                    <template #prefix>
                        <Plus class="h-3 w-3 stroke-1.5" />
                    </template>
                    {{ __('New') }}
                </Button>
            </div>
        </div>
        <div v-if="teamsAccounts.data?.length" class="overflow-y-scroll">
            <ListView
                :columns="columns"
                :rows="teamsAccounts.data"
                row-key="name"
                :options="{
                    showTooltip: false,
                    onRowClick: (row) => {
                        openForm(row.name)
                    },
                }"
            >
                <ListHeader
                    class="mb-2 grid items-center space-x-4 rounded bg-surface-gray-2 p-2"
                >
                    <ListHeaderItem :item="item" v-for="item in columns">
                        <template #prefix="{ item }">
                            <FeatherIcon
                                v-if="item.icon"
                                :name="item.icon"
                                class="h-4 w-4 stroke-1.5"
                            />
                        </template>
                    </ListHeaderItem>
                </ListHeader>

                <ListRows>
                    <ListRow :row="row" v-for="row in teamsAccounts.data">
                        <template #default="{ column, item }">
                            <ListRowItem :item="row[column.key]" :align="column.align">
                                <div v-if="column.key == 'enabled'">
                                    <Badge v-if="row[column.key]" theme="green">
                                        {{ __('Enabled') }}
                                    </Badge>
                                    <Badge v-else theme="gray">
                                        {{ __('Disabled') }}
                                    </Badge>
                                </div>
                                <div v-else class="leading-5 text-sm">
                                    {{ row[column.key] }}
                                </div>
                            </ListRowItem>
                        </template>
                    </ListRow>
                </ListRows>
            </ListView>
        </div>
    </div>
    <TeamsAccountModal
        v-model="showForm"
        v-model:teamsAccounts="teamsAccounts"
        :accountID="currentAccount"
    />
</template>
<script setup>
import {
    Badge,
    Button,
    createListResource,
    FeatherIcon,
    ListView,
    ListHeader,
    ListHeaderItem,
    ListRows,
    ListRow,
    ListRowItem,
} from 'frappe-ui'
import { computed, ref } from 'vue'
import { Plus } from 'lucide-vue-next'
import TeamsAccountModal from '@/components/Modals/TeamsAccountModal.vue'

const showForm = ref(false)
const currentAccount = ref(null)

const props = defineProps({
    label: String,
    description: String,
})

const teamsAccounts = createListResource({
    doctype: 'LMS Teams Settings',
    fields: ['name', 'enabled', 'member', 'account_name'],
    auto: true,
})

const openForm = (accountID) => {
    currentAccount.value = accountID
    showForm.value = true
}

const columns = computed(() => {
    return [
        { label: __('Account Name'), key: 'account_name', icon: 'video' },
        { label: __('Member'), key: 'member', icon: 'user' },
        { label: __('Status'), key: 'enabled', align: 'center', icon: 'check-square' },
    ]
})
</script>