from prefect import flow

@flow
def test_functions():
    print("HELLO FROM THE FLOW FUNCTION")

if __name__ == "__main__":
    print('hello from main')
