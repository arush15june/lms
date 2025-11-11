<template>
    <Dialog
        v-model="show"
        :options="{
            title:
                accountID === 'new' ? __('New Teams Account') : __('Edit Teams Account'),
            size: 'xl',
            actions: [
                {
                    label: __('Save'),
                    variant: 'solid',
                    onClick: ({ close }) => {
                        saveAccount(close)
                    },
                },
            ],
        }"
    >
        <template #body-content>
            <div class="mb-4">
                <FormControl
                    v-model="account.enabled"
                    :label="__('Enabled')"
                    type="checkbox"
                />
            </div>
            <div class="grid grid-cols-2 gap-5">
                <FormControl
                    v-model="account.account_name"
                    :label="__('Account Name')"
                    type="text"
                    :required="true"
                />
                <Link
                    v-model="account.member"
                    :label="__('Member')"
                    doctype="User"
                    :required="true"
                />
                <FormControl
                    v-model="account.tenant_id"
                    :label="__('Tenant ID')"
                    type="text"
                    :required="true"
                />
                <FormControl
                    v-model="account.client_id"
                    :label="__('Client ID')"
                    type="text"
                    :required="true"
                />
                <FormControl
                    v-model="account.client_secret"
                    :label="__('Client Secret')"
                    type="password"
                    :required="true"
                />
            </div>
        </template>
    </Dialog>
</template>
<script setup>
import { call, Dialog, FormControl, toast, Button } from 'frappe-ui'
import { inject, reactive, watch } from 'vue'
import { cleanError } from '@/utils'
import Link from '@/components/Controls/Link.vue'

const show = defineModel('show')
const user = inject('$user')
const teamsAccounts = defineModel('teamsAccounts')

const account = reactive({
    name: '',
    enabled: false,
    member: user?.data?.name || '',
    account_name: '',
    tenant_id: '',
    client_id: '',
    client_secret: '',
})

const props = defineProps({
    accountID: {
        type: String,
        default: 'new',
    },
})

watch(
    () => props.accountID,
    (val) => {
        if (val != 'new') {
            teamsAccounts.value?.data.forEach((acc) => {
                if (acc.name === val) {
                    Object.assign(account, acc)
                }
            })
        }
    }
)

watch(show, (val) => {
    if (!val) {
        Object.assign(account, {
            name: '', enabled: false, member: user?.data?.name || '',
            account_name: '', tenant_id: '', client_id: '', client_secret: ''
        })
    }
})

const saveAccount = (close) => {
    if (props.accountID == 'new') {
        createAccount(close)
    } else {
        updateAccount(close)
    }
}

const createAccount = (close) => {
    teamsAccounts.value?.insert.submit(
        { ...account },
        {
            onSuccess() {
                teamsAccounts.value?.reload()
                close()
                toast.success(__('Teams Account created successfully'))
            },
            onError(err) {
                close()
                toast.error(cleanError(err.messages[0]) || __('Error creating Teams Account'))
            },
        }
    )
}

const updateAccount = async (close) => {
    if (props.accountID != account.account_name) {
        await renameDoc()
    }
    setValue(close)
}

const renameDoc = async () => {
    await call('frappe.client.rename_doc', {
        doctype: 'LMS Teams Settings',
        old_name: props.accountID,
        new_name: account.account_name,
    })
}

const setValue = (close) => {
    teamsAccounts.value?.setValue.submit(
        { ...account, name: account.account_name },
        {
            onSuccess() {
                teamsAccounts.value?.reload()
                close()
                toast.success(__('Teams Account updated successfully'))
            },
            onError(err) {
                close()
                toast.error(cleanError(err.messages[0]) || __('Error updating Teams Account'))
            },
        }
    )
}
</script>