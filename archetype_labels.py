archetype_to_example = {
    'Warlock-Handlock'              : 'AAECAf0GBPIFqa0C08UCl9MCDTCKAbYH4QeNCMQIzAjzDN28At7EAufLAvfNApfoAgA=',
    'Warlock-Krul'                  : 'AAECAf0GHooB9wTtBfIFiQbbBooHkge2B+EH+weNCMQIzAjzDNi7ArC8Atm8At28Av2/ApvCAuTCAsrDAt7EAtPFAufLAqLNAvfNAsLOApfTAgAA',
    'Warrior-Pirate'                : 'AAECAQcCyAORvAIOHLACkQP/A44FqAXUBfIF7gbnB+8HgrACiLACr8ICAA==',
    'Warrior-Taunt'                 : 'AAECAQcGkAO5sgLTwwKixwLMzQLCzgIMS5ED1ASRBvsMgq0C/rwCm8ICxsMCysMC38QCyccCAA==',
    'Paladin-Mid_Murloc'            : 'AAECAYsWBqEG+ga8vQLjvgK5wQLvwgIM2wOvB6cI06oC2a4Cs8ECncICscICiMcC48sCps4ClugCAA==',
    'Paladin-Control'               : 'AAECAaToAg7yBc8G+gbbCvsMiq4C2a4C5q4CubICvL0CucEC08UCyccCjtMCCIoB3AP0BfYHjwmzwQKbwgKIxwIA',
    'Paladin-Aggro_Shield'          : 'AAECAaToAgbUBZG8Ary9ArnBAuvCApziAgxG8gGnBfUFzwbuBq8H5QfZrgK6vQLjywKVzgIA',
    'Druid-Jade'                    : 'AAECAZICBvIFrqsClL0C08UCyccCmdMCDEBfigH+AcQG5Ai0uwLLvALPvALdvgKgzQKHzgIA',
    'Rogue-Mid_Combo'               : 'AAECAaIHCLICzQOvBO0FkbwCyb8C/MECgsICC7QBjAKbBZcGiAekB4YJkrYC9bsCgcICm8gCAA==',
    'Rogue-Elemental'               : 'AAECAYO6AgrtArsD1AWRvALJvwKZwgLCzgKU0AKa4gKc4gIKtAHdCNyvApK2AoHCAqzCAuvCAsrDAsjHAqbOAgA=',
    'Mage-Secret'                   : 'AAECAY0WCMAB7gLsB7gIobcC+r8C08UC3s0CC3G7ApUDqwSWBewFo7YC17YCh70CwcECmMQCAA==',
    'Mage-Freeze'                   : 'AAECAf0ECMUE7QTtBewHuAi/CIivAtPFAguKAcABuwLJA6sEywSWBfsM17YCwcECmMQCAA==',
    'Mage-Quest'                    : 'AAECAc2xAgTtBLgI0MECudECDYoBwAH7AZwCyQOrBMsE5gT4B5KsAsHBApjEAtrFAgA=',
    'Mage-Tempo_Burn'               : 'AAECAf0EBsABuAi/COm6AuTCAtPFAgxxuwKLA5UDqwSWBewFo7YC17YC+r8CwcECmMQCAA==',
    'Shaman-Evolve'                 : 'AAECAaoIBJG8ApS9ApvLAuvPAg2BBOUH8AeTCfqqAvuqAqC2Aoe8AtG8Ava9Avm/ApHBAuvCAgA=',
    "Shaman-Big_N'Zoth"             : 'AAECAaoIDKQDkwT1BO0F9QiiCeCsAsKuAqa8ArHEAtPFAsLOAgmKAZQD/gX7DKC2At26Ava9AsfBApvCAgA=',
    "Shaman-N'Zoth"                 : 'AAECAaoICKQD7QWyBvsM4KwCprwClL0Cis4CC/UE/gWgtgLdugKHvALPvALRvAL2vQLHwQKbwgKHxAIA',
    'Priest-Razakus'                : 'AAECAa0GHgmKAfsBkAKXAuUE7QXJBqUJ0wrXCvIM+wyhrAKStAKDuwK1uwK3uwLYuwKwvALhvwLovwLqvwLRwQLYwQLZwQLTxQK+yALwzwKQ0wIAAA==',
    'Priest-Silence'                : 'AAECAZ/HAgTSCvsMtbsCvsgCDfgC3QTlBKUJ0QrXCvIMqa0CrLQC8LsC0cEC2MECxccCAA==',
    'Priest-Hemet_Razakus_Sil'      : 'AAECAa0GCqUJ0wr7DIO7ArW7Auq/Ap3HAs/HAr7IApDTAgr4AuUE9gfRCtIK8gzwuwLRwQLYwQLKwwIA',
    'Priest-Big'                    : 'AAECAa0GBKIJqKsChbgCws4CDaUJ0wrXCqGsAqKsApK0ArW7Aui/Auq/AtHBAuXMAubMArTOAgA=',
}

example_to_archetype = {}
for i, j in archetype_to_example.items():
    example_to_archetype[j] = i
