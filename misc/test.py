#!/usr/bin/env python


from backtranslate.backtranslate import (
    reverse_translation_table, one_subst_without_dna, one_subst)


back_table = reverse_translation_table(1)

result = set()
for aa1 in back_table:
    for aa2 in back_table:
        p = one_subst_without_dna(back_table, aa1, aa2)
        for codon in back_table[aa1]:
            q = one_subst(back_table, codon, aa2)
            #print aa1, aa2, p, codon, q,
            if q and str(p) != str(q) and aa1 != aa2:
                #print '<--',
                result.add((aa1, aa2))
            #print

print result
