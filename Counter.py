class Counter():
    """
    A counter which continually counts up from 0.
    """
    count = 0

    def get_next(self):
        """
        Gets the next number from the counter.
        """
        next_num = self.count
        self.count += 1
        return next_num