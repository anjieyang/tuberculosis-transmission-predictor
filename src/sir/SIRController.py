import numpy as np
import pandas as pd
from tqdm import tqdm


class SIRController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def simulate(self):
        for t in tqdm(range(1, self.model.time_steps), total=self.model.time_steps, desc='Simulating'):
            # traverse the current group
            for current in range(len(self.model.sir_groups)):
                dS_current = 0
                current_group = self.model.sir_groups[current]

                # get the current b
                kappa, tau, gamma = self.model.parameter[current]
                b = kappa * tau

                # get the initial
                current_S = self.model.S[current][t - 1]
                current_I = self.model.I[current][t - 1]
                current_R = self.model.R[current][t - 1]

                # divide the susceptible into stay and out
                stay_S_current = current_S * current_group.get_contacts_proportion(current)

                stay_I_current = current_I * current_group.get_contacts_proportion(current)

                stay_N_current = current_group.population * current_group.get_contacts_proportion(current)

                # calculate the dS of the stay people
                dS_stay_current = b * stay_S_current * stay_I_current / stay_N_current

                # the dS_stay should never exceed stay S
                dS_stay_current = dS_stay_current if dS_stay_current <= stay_S_current else stay_S_current

                dS_current += dS_stay_current

                # calculate the dS of the out people
                for contact in range(len(self.model.sir_groups)):
                    if current_group.get_contacts_proportion(contact) == 0 or contact == current:
                        continue

                    contact_group = self.model.sir_groups[contact]

                    # get the initial
                    contact_S = self.model.S[current][t - 1]
                    contact_I = self.model.I[contact][t - 1]

                    pr_S_current = current_S * current_group.get_contacts_proportion(contact)
                    pr_I_current = current_I * current_group.get_contacts_proportion(contact)
                    pr_N_current = current_group.population * current_group.get_contacts_proportion(contact)

                    pr_S_contact = contact_S * contact_group.get_contacts_proportion(current)
                    pr_I_contact = contact_I * contact_group.get_contacts_proportion(current)
                    pr_N_contact = contact_group.population - current_group.get_contacts_proportion(current)

                    # build the party room
                    pr_S = pr_S_current + pr_S_contact
                    pr_I = pr_I_current + pr_I_contact
                    pr_N = pr_N_current + pr_N_contact

                    # calculate the dS of the partyroom people
                    dS_pr = b * pr_S * pr_I / pr_N

                    # the dS_partyroom should never exceed partyroom S
                    dS_pr = dS_pr if dS_pr <= pr_S else pr_S

                    dS_pr_current = dS_pr * pr_N_current / pr_N

                    # assign the value
                    dS_current += dS_pr_current

                # anomaly detection
                dS_current = dS_current if dS_current <= current_S else current_S

                current_S -= dS_current
                current_I += dS_current

                # calculate the dI of current group
                dI_current = current_I * gamma

                # assign the value
                current_I -= dI_current
                current_R += dI_current

                # update the value
                self.model.S[current][t] = current_S
                self.model.I[current][t] = current_I
                self.model.R[current][t] = current_R

        transposed_S = np.transpose(self.model.S)
        transposed_I = np.transpose(self.model.I)
        transposed_R = np.transpose(self.model.R)

        # Create a DataFrame for each array
        df1 = pd.DataFrame(transposed_S)
        df2 = pd.DataFrame(transposed_I)
        df3 = pd.DataFrame(transposed_R)

        contacts_arrays = []
        for group in self.model.sir_groups:
            contacts_arrays.append(group.contacts)

        combined_array = np.vstack(contacts_arrays)

        transposed_combined = np.transpose(combined_array)

        dftc = pd.DataFrame(transposed_combined)

        writer = pd.ExcelWriter('./sir/data.xlsx', engine='xlsxwriter')

        # Write each DataFrame to a different worksheet
        df1.to_excel(writer, sheet_name='S', index=False)
        df2.to_excel(writer, sheet_name='I', index=False)
        df3.to_excel(writer, sheet_name='R', index=False)
        dftc.to_excel(writer, sheet_name='contacts', index=False)

        # Save the Excel file
        writer.close()

        print('Completed!')

        self.view.show_view()
