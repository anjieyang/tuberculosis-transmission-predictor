import numpy as np
import pandas as pd
from tqdm import trange

from src.sir.Generator import Generator
from src.sir.SIRModel import SIRModel
from src.sir.SIRView import SIRView


class SIRController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def simulate(self):
        for t in trange(1, self.model.time_steps):
            # traverse the current group
            for current in range(len(self.model.groups)):
                dS_current = 0
                current_group = self.model.groups[current]

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
                for contact in range(current + 1, len(self.model.groups)):
                    # check if they have contact
                    if current_group.get_contacts_proportion(contact) == 0:
                        continue

                    contact_group = self.model.groups[contact]

                    # get the initial
                    contact_S = self.model.S[current][t - 1]
                    contact_I = self.model.I[contact][t - 1]
                    contact_R = self.model.R[contact][t - 1]

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
                    dS_pr_contact = dS_pr * pr_N_contact / pr_N

                    # assign the value
                    dS_current += dS_pr_current

                    contact_S -= dS_pr_contact
                    contact_I += dS_pr_contact

                    # update the value
                    self.model.S[contact][t] = contact_S
                    self.model.I[contact][t] = contact_I
                    self.model.R[contact][t] = contact_R

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

        writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')

        # Write each DataFrame to a different worksheet
        df1.to_excel(writer, sheet_name='S', index=False)
        df2.to_excel(writer, sheet_name='I', index=False)
        df3.to_excel(writer, sheet_name='R', index=False)

        # Save the Excel file
        writer.close()

        contacts_arrays = []
        for group in self.model.groups:
            contacts_arrays.append(group.contacts)

        combined_array = np.vstack(contacts_arrays)

        transposed_combined = np.transpose(combined_array)

        dftc = pd.DataFrame(transposed_combined)

        writer = pd.ExcelWriter('contacts.xlsx', engine='xlsxwriter')

        dftc.to_excel(writer, sheet_name='data', index=False)

        writer.close()

        print('Completed!')

        self.view.show_view()


if __name__ == '__main__':
    groups = Generator.generate_sir_groups(5, 0)
    sir_model = SIRModel(groups, 100)
    sir_view = SIRView('')
    sir_controller = SIRController(sir_model, sir_view)

    sir_controller.simulate()