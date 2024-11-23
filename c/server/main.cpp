int main() {
    try {
        NonBlockingRobotControl robot(true);
        
        // Mantém o programa rodando até receber comando de shutdown
        while (robot.isRunning()) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    } catch (const std::exception& e) {
        std::cerr << "Erro: " << e.what() << std::endl;
    }
    return 0;
}
