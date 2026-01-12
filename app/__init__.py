from app.agents.emem import respond as emem_respond
from app.agents.tolu import respond as tolu_respond
from app.agents.sola import respond as sola_respond
from app.agents.kemi import respond as kemi_respond


AGENT_REGISTRY = {
    "Emem": emem_respond,
    "Tolu": tolu_respond,
    "Sola": sola_respond,
    "Kemi": kemi_respond,
}
