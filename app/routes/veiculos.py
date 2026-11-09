from fastapi import APIRouter, Path
from app.schemas import VeiculosResponse, Veiculo
from app.database import obter_veiculos_por_motorista

router = APIRouter(prefix="/api/v1/veiculos", tags=["Veículos"])


@router.get(
    "/{id_motorista}",
    response_model=VeiculosResponse,
    summary="Listar Veículos do Motorista",
    description="Retorna a lista de caminhões/veículos vinculados à conta do motorista."
)
def listar_veiculos(
    id_motorista: int = Path(..., gt=0, description="ID numérico do motorista")
):
    veiculos_data = obter_veiculos_por_motorista(id_motorista)
    lista_veiculos = [Veiculo(**v) for v in veiculos_data]

    return VeiculosResponse(
        id_motorista=id_motorista,
        total=len(lista_veiculos),
        veiculos=lista_veiculos
    )
