archetype_to_example = {
    "Aggro Druid"                   : 'AAECAZICAtkHkbwCDvcD5gXlB8GrArazAs27AobBAq/CAuTCAuvCApvNApHQAvvTAovlAgA=',
    "Big Druid"                     : 'AAECAZICCsIGogmfsALguwLJxwLCzgKZ0wLm0wL94QLx6gIKQF/EBuQIvq4Cy7wC+cACoM0Ch84C3esCAA==',
    "Jade Druid"                    : 'AAECAZICBpAHrqsCvq4C4LsClL0CmdMCDEBfxAbkCLS7Asu8As+8At2+AqDNAofOAqbOAvvTAgA=',
    "Quest Druid"                   : 'AAECAZICBrQD4LsCi8ECmNICntICmdMCDEBf0wOTBMQG5AjLvAKgzQKHzgL70wKa5AKE5gIA',

    "Big Priest"                    : 'AAECAZ/HAgaiCaUJqKsChbgCws4CkNMCDNMK1wqhrAK3uwLovwLqvwLRwQLlzALmzAK0zgLo0ALj6QIA',
    "Highlander Priest"             : 'AAECAZ/HAh4J7QH7AZcCnAKhBOUE7QWQB6QH9gelCdIK0wrWCtcK8gz7DJK0AoO7ArW7Ati7Auq/AtHBAtLBAtjBAtnBAvDPAujQApDTAgAA',
    "Spiteful Summoner Priest"      : 'AAECAa0GAo0I0OcCDgjyDIK1Arq7AvC7AtnBAsrDApnIAsrLAs7MAqbOAvvTAsvmAtfrAgA=',

    "Tempo Rogue"                   : 'AAECAYO6AgayAq8E1AWRvAKbywKc4gIMtAHtAqgF8gXdCJK2AoHCAuvCAsrLAqbOAvvTAtvjAgA=',

    "Cube Warlock"                  : 'AAECAcn1AgKX0wLb6QIOkwT3BPIFtgfhB8QI3sQC58sC8tAC+NACiNICi+EC/OUC6OcCAA==',
    "Cube Demon Warlock"            : 'AAECAf0GCPIFigfECMwIycICl9MCl+gC2+kCC/cE2wa2B97EAufLAvLQAvjQAojSAovhAvzlAujnAgA=',
    "Demon Warlock"                 : 'AAECAf0GBooH4KwCz8cCrs0Cl9MC2OcCDNsGtgfECMwIysMC3sQC58sC8tAC+NACiNIC/OUC6OcCAA==',

    "Secret Mage"                   : 'AAECAf0EBsABqwS/CKO2AqLTAvvTAgxxuwKVA+YElgXsBde2Auu6Aoe9AsHBApjEAo/TAgA=',

    "Aggro Hunter"                  : 'AAECAR8EjQGvBKgFkbwCDagCtQPUBdkH6wfbCf4M6rsCjsMC3dIC+9MC4eMCi+UCAA==',
    "Summoner Hunter"               : 'AAECAR8EuwWRvALKywLQ5wINqAXUBdkH6wf+DMeuAuq7Ao7DAtfNAvvTAuHjAovlAtfrAgA=',

    "Murloc Paladin"                : 'AAECAYsWBq8H2a4C474CucEC5MICps4CDMUD2wOnCNOqAtO8ArPBAp3CArHCAuPLAvjSAvvTAtblAgA=',
    "Aggro Paladin"                 : 'AAECAZ8FBK8EzwaRvAK5wQINpwXUBfUFrwfZB7EI2a4CuMcC48sClc4C+NIC+9MC1uUCAA==',
    "Summoner Aggro Paladin"        : 'AAECAZ8FBOO+ArPBArnBAsrLAg3bA6cIjwnTqgLZrgKqwQKdwgKxwgLjywKmzgL40gL70wLX6wIA',
    
}

example_to_archetype = {}
for i, j in archetype_to_example.items():
    example_to_archetype[j] = i
