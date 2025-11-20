def get_board_id(id, boards):
    for board in boards:
        if board["id"] == id:
            return board
    return {"message": "no content"}
