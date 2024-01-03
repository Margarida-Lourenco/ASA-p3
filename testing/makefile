# Por aqui caminho relativo para o codigo
SCRIPT=src/main.py
# Por aqui caminho relativo para a pasta dos testes
TESTS_DIR=tests

# Daqui para a frente ja nao e preciso mudar nada :)

# ==Comandos==
# make test para correr os testes
# make clean para apagar os resultados
# make checkpy para verificar a versao de python que esta a ser usada
# python3.7 e o usado no mooshak (especificamente 3.7.3)
# se nao estiver presente, python3 sera usado
# ==Resultados==
# Os resultados ficam na pasta test_res, divididos em 4 ficheiros
# 00_diff contem o diff entre o esperado e o obtido
# test_expected_out mostra o resultado esperado
# test_effective_out mostra o resultado obtido
# test_order mostra a ordem pela qual os testes foram corridos

#==Code==

TESTS=$(wildcard $(TESTS_DIR)/*.in)
RESULTS=$(patsubst %.in,%.out,$(TESTS))
PY=python3

ifneq ($(shell which python3.7),)
	PY=python3.7
endif

.PHONY: all test clean checkpy

all: test
test:
	@echo "Running tests..."
	@mkdir -p test_res
	@echo "" > test_res/test_effective_out
	@-for testfile in $(TESTS) ; do \
		$(PY) $(SCRIPT) < $$testfile >> test_res/test_effective_out; \
	done
	@echo "" > test_res/test_expected_out
	@-for resultfile in $(RESULTS) ; do \
		cat $$resultfile >> test_res/test_expected_out; \
	done
	@echo "" > test_res/test_order
	@-for testfile in $(TESTS) ; do \
		echo $$testfile >> test_res/test_order; \
	done
	@(diff test_res/test_effective_out test_res/test_expected_out > test_res/00_diff && echo "Tests passed.") || echo "Some tests failed."

clean:
	$(RM) -r test_res

checkpy:
	@echo $(PY)
