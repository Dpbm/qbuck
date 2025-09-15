#include <iostream>
#include <random>

#include <pybind11/pybind11.h>

namespace py = pybind11;

class RandomUtility{
    public:
        void random_seed(){
            std::cout << "generating seed....\n";
            this->set_seed(this->rd());
        }

        void set_seed(size_t new_seed){
            std::cout << "Setting seed to: " << new_seed << "\n";
            this->seed = new_seed;
            this->rng.seed(new_seed);
        }

        size_t get_random_value(){
            // both 0 and 1 has 50% of chance
            return std::discrete_distribution<size_t>({0.5, 0.5})(this->rng);
        }

        size_t get_seed() const {
            return this->seed;
        }


    private:
        std::mt19937_64 rng;
        std::random_device rd;
        size_t seed;
};


PYBIND11_MODULE(random_utility, m, py::mod_gil_not_used()) {
    py::class_<RandomUtility>(m, "RandomUtility")
        .def(py::init<>())
        .def("random_seed", &RandomUtility::random_seed)
        .def("set_seed", &RandomUtility::set_seed)
        .def("get_random_value", &RandomUtility::get_random_value)
        .def_property_readonly("seed", &RandomUtility::get_seed);
}
